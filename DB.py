import cx_Oracle
import pandas as pd
import re
import os
import json
import time
from main import obtener_informacion_ticket


def load_config(filename='uenocore_config.json'):
    """
    Carga la configuración de la base de datos desde un archivo JSON.
    """
    with open(filename) as f:
        config = json.load(f)
    return config['db_config']


def connect_to_database(config):
    """
    Establece una conexión a la base de datos utilizando la configuración proporcionada.
    """
    dsn = config['dsn']
    username = config['username']
    password = config['password']
    connection = cx_Oracle.connect(username, password, dsn=dsn)
    return connection


def create_output_folder(output_folder):
    """
    Crea la carpeta de salida si no existe.
    """
    os.makedirs(output_folder, exist_ok=True)


def extract_queries(raw_text):
    """
    Extrae consultas SELECT, INSERT, DELETE, y UPDATE del texto bruto.
    """
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    select_queries, insert_queries, delete_queries, update_queries = [], [], [], []
    query_accumulator = []

    for line in lines:
        line_without_comment = re.sub(r'--.*$', '', line).strip()
        if line_without_comment:
            query_accumulator.append(line_without_comment)

        if ';' in line_without_comment:
            query_accumulator_str = ' '.join(query_accumulator).rstrip(';').strip()

            if re.match(r'^\s*insert', query_accumulator_str, re.IGNORECASE):
                insert_queries.append(query_accumulator_str)
            elif re.match(r'^\s*select', query_accumulator_str, re.IGNORECASE):
                select_queries.append(query_accumulator_str)
            elif re.match(r'^\s*delete', query_accumulator_str, re.IGNORECASE):
                delete_queries.append(query_accumulator_str)
            elif re.match(r'^\s*update', query_accumulator_str, re.IGNORECASE):
                update_queries.append(query_accumulator_str)

            query_accumulator = []

    return select_queries, insert_queries, delete_queries, update_queries


def execute_select_queries(connection, select_queries, output_folder, jira_number):
    """
    Ejecuta consultas SELECT y guarda los resultados en un archivo Excel.
    """
    results_df = pd.DataFrame()

    if select_queries:
        try:
            with pd.ExcelWriter(os.path.join(output_folder, f'{jira_number}.xlsx'), engine='xlsxwriter') as excel_writer:
                for idx, select_query in enumerate(select_queries):
                    table_name_match = re.search(r'from\s+(\w+)', select_query, re.IGNORECASE)
                    table_name = table_name_match.group(1) if table_name_match else f'Sheet_{idx + 1}'

                    existing_sheets = excel_writer.sheets.keys()
                    original_table_name = table_name
                    suffix_number = 1

                    while table_name in existing_sheets:
                        table_name = f'{original_table_name}_Dup{suffix_number}'
                        suffix_number += 1

                    with connection.cursor() as cursor:
                        cursor.execute(select_query)
                        result_set = cursor.fetchall()

                        # Crear DataFrame con las columnas y manejar duplicados
                        df = pd.DataFrame(result_set, columns=[desc[0] for desc in cursor.description])
                        df.columns = pd.io.parsers.ParserBase({'names': df.columns})._maybe_dedup_names(df.columns)

                        # Escribir datos en Excel
                        df.to_excel(excel_writer, sheet_name=table_name, index=False)

                        # Ajustar el ancho de las columnas
                        worksheet = excel_writer.sheets[table_name]
                        for i, col in enumerate(df.columns):
                            try:
                                max_data_len = df[col].dropna().astype(str).map(len).max() if not df[col].empty else 0
                            except Exception:
                                max_data_len = 0

                            max_len = max(max_data_len, len(col)) + 2
                            worksheet.set_column(i, i, max_len)

                        # Concatenar DataFrame para resultados acumulados
                        results_df = pd.concat([results_df, df], ignore_index=True) if not results_df.empty else df.copy()

            print("-" * 33)
            print(f"|{'BACKUP OK':^31}|")
            print("-" * 33)

        except cx_Oracle.DatabaseError as e:
            print(f"Error al ejecutar los comandos: {e}")
            connection.rollback()

    else:
        print("-" * 22)
        print(f"|{'NO BACKCUP':^20}|")
        print("-" * 22)

    return results_df

#esta parte del codigo cumple con una funcion especifica de una base de datos llamada ITGF, mandando el link del fsop como comentario para AUDITORIA, si no es necesario se borra y ya está 
def execute_module_begin(connection, fsop):
    """
    Ejecuta el módulo begin con el número de FSOP dado.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                begin
                    pre_ini_aplicacion;
                    pae_cnf.G_COD_MODULO:=1;
                end;
                --{fsop}
            """)
    except cx_Oracle.DatabaseError as e:
        print(f"Error al ejecutar el módulo begin: {e}")


def execute_queries(delete_queries, insert_queries, update_queries, connection):
    """
    Ejecuta consultas DELETE, INSERT, y UPDATE.
    """
    for delete_query in delete_queries:
        try:
            with connection.cursor() as cursor:
                start_time = time.time()
                cursor.execute(delete_query)
                end_time = time.time()
                execution_time = end_time - start_time

                rows_affected = cursor.rowcount

                print(delete_query)

                if rows_affected >= 300:
                    print(f"Rollback please check query, rows affected => {rows_affected}, done in {execution_time:.3f} seconds")
                    print('-' * 15)
                    connection.rollback()
                else:
                    print(f"Commit: rows affected => {rows_affected}, done in {execution_time:.3f} seconds")
                    print('-' * 15)
                    connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('-' * 15)
            print(delete_query)
            print(" ")
            print(f"Error: {e}")
            print('-' * 15)
            connection.rollback()

    for insert_query in insert_queries:
        try:
            with connection.cursor() as cursor:
                start_time = time.time()
                cursor.execute(insert_query)
                end_time = time.time()
                execution_time = end_time - start_time

                rows_affected = cursor.rowcount

            print(insert_query)
            connection.commit()
            print(f"Commit: Rows affected => {rows_affected}, done in {execution_time:.3f} seconds")
            print('-' * 15)

        except cx_Oracle.DatabaseError as e:
            print('-' * 15)
            print(insert_query)
            print(" ")
            print(f"Error: {e}")
            print('-' * 15)
            connection.rollback()

    for update_query in update_queries:
        try:
            with connection.cursor() as cursor:
                start_time = time.time()
                cursor.execute(update_query)
                end_time = time.time()
                execution_time = end_time - start_time

                rows_affected = cursor.rowcount

                print(update_query)

                if rows_affected >= 300:
                    print(f"Rollback please check query, rows affected => {rows_affected}, done in {execution_time:.3f} seconds")
                    print('-' * 15)
                    connection.rollback()
                else:
                    print(f"Commit: rows affected => {rows_affected}, done in {execution_time:.3f} seconds")
                    print('-' * 15)
                    connection.commit()

        except cx_Oracle.DatabaseError as e:
            print("-" * 15)
            print(update_query)
            print(" ")
            print(f"Error: \n {e}")
            print('-' * 15)
            connection.rollback()


def main(jira_number_digits, raw_text):
    """
    Función principal del programa.
    """
    print('Current Database: UENOCORE')

    # Cargar la configuración de la base de datos
    config = load_config()

    # Conectar a la base de datos
    connection = connect_to_database(config)

    # Crear la carpeta de salida
    create_output_folder(r'C:\IT\BK_FSOP')

    jira_number = f'{jira_number_digits}'

    # Extraer las consultas del texto
    select_queries, insert_queries, delete_queries, update_queries = extract_queries(raw_text)

    # Ejecutar las consultas SELECT y almacenar resultados en Excel
    if select_queries:
        results_df = execute_select_queries(connection, select_queries, r'C:\IT\BK_FSOP', jira_number)
    else:
        print("-" * 22)
        print(f"|{'NO BACKCUP':^20}|")
        print("-" * 22)

    # Ejecutar módulo begin
    execute_module_begin(connection, jira_number_digits)

    # Ejecutar consultas DELETE, INSERT y UPDATE
    execute_queries(delete_queries, insert_queries, update_queries, connection)

    print("-" * 33)
    print(f"|{'Execution Ended':^31}|")
    print("-" * 33)


if __name__ == "__main__":
    print("Este script no debe ejecutarse directamente.")
    print("Por favor, ejecute execute.py en su lugar.")
