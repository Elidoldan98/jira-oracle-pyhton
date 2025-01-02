from jira import JIRA
import bkuenocore
import os

def obtener_informacion_ticket(ticket_id, jira):
    ticket_key = f"FSOP-{ticket_id}"
    try:
        ticket = jira.issue(ticket_key)
        descripcion = ticket.fields.description
        estado_actual = ticket.fields.status.name  # Obtén el estado actual del ticket
        asignado = ticket.fields.assignee
        print(f"Esta es la persona asignada {asignado}")
        return descripcion, estado_actual, ticket
    except Exception as e:
        return None, None, f"Error al obtener el ticket: {str(e)}"

def realizar_transicion(ticket, jira, transicion_nombre):
    try:
        transitions = jira.transitions(ticket)
        for transition in transitions:
            if transition['name'] == transicion_nombre:
                jira.transition_issue(ticket, transition['id'])
                print(f"Transición '{transicion_nombre}' realizada con éxito.")
                return True
        print(f"No se encontró la transición '{transicion_nombre}'.")
        return False
    except Exception as e:
        print(f"Error al realizar la transición: {str(e)}")
        return False
#el estado de los tickets, depende del proyecto, en este caso estan en un proyecto con GTI pero pueden ser cambiados
def cambiar_estado_ticket(estado_actual, ticket, jira):
    if estado_actual == "Pendiente Aprobacion GTI":
        realizar_transicion(ticket, jira, "Ejecutado. Pendiente aprobación GTI")
    elif estado_actual == "APROBADO":
        if realizar_transicion(ticket, jira, "EN EJECUCIÓN"):
            realizar_transicion(ticket, jira, "FINALIZADO")
    elif estado_actual == "APROBADO PEND. FINALIZACION":
        realizar_transicion(ticket, jira, "FINALIZADO")
    else:
        print("El estado actual no requiere cambios.")

def asignarse_ticket(ticket, jira):
    persona_asignada = ticket.fields.assignee
    if persona_asignada is None or persona_asignada.displayName != "USER":
        try:
            # Asignar el ticket al usuario en cuestion
            usuario_asignado = "USER"  # Cambia esto al nombre de usuario correcto en JIRA
            jira.assign_issue(ticket, usuario_asignado)
            print(f"Ticket '{ticket.key}' asignado a '{usuario_asignado}'.")
            return True
        except Exception as e:
            print(f"Error al asignar el ticket: {str(e)}")
            return False
    else:
        print("El ticket ya está asignado.")
        return False

def agregar_comentario_con_adjunto(ticket, jira, file_path):
    comentario_texto = "Ejecutado"
    jira.add_comment(ticket, comentario_texto)
    print(f"Comentando 'Ejecutado' en el ticket")

    # Adjuntar el archivo al ticket
    try:
        jira.add_attachment(issue=ticket, attachment=file_path)
        print(f"Archivo '{file_path}' adjuntado al ticket.")
       
    except Exception as e:
        print(f"Error al adjuntar el archivo: {str(e)}")

def agregar_comentario(ticket, jira):
    comentario_texto = "Ejecutado "
    try:
        jira.add_comment(ticket, comentario_texto)
        print(f"Comentando '{comentario_texto}' en el ticket.")
    except Exception as e:
        print(f"Error al comentar el ticket: {str(e)}")
        
        
#En esta funcion se agrega el token de jira, generado por usuario en la plataforma. 
def main():
    jira = JIRA(server="https://PROYECTO.atlassian.net", 
                basic_auth=("USER_MAIL", 
                            "TOKEN CODE"))

    print("JIRA_ORACLE_PYHTON 1.0")
    while True:
        ticket_id = input("¿Cual es el FSOP?: ")
        print("Buscando...")
        if len(ticket_id) == 5 and ticket_id.isdigit():
            break
        print("Error: Debe ingresar exactamente 5 dígitos.")
    
    descripcion, estado_actual, ticket = obtener_informacion_ticket(ticket_id, jira)
    
    if not descripcion:
        print(estado_actual)  # Imprime el error si no se pudo obtener el ticket
        return

    print(f"Encontré estas sentencias en el ticket:\n{descripcion}")
    print(f"Estado actual del ticket: {estado_actual}")
    print("-" * 22)
    
    ejecutar = input("¿Querés que ejecute estas sentencias? (sí/no): ")
    if ejecutar.lower() in ["sí", "si", "s"]:
        bkuenocore.main(ticket_id, descripcion)
        
        # Ruta al archivo Excel generado
        file_path = os.path.join(r'C:\IT\BK_FSOP', f'{ticket_id}.xlsx')
        
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            agregar_comentario_con_adjunto(ticket, jira, file_path)
        else:
            print(f"Archivo '{file_path}' no encontrado, comentando sin adjuntar.")
            agregar_comentario(ticket, jira)
        
        # Cambiar el estado del ticket según las reglas definidas
        cambiar_estado_ticket(estado_actual, ticket, jira)
        
        # Asignar el ticket si es necesario
        asignarse_ticket(ticket, jira)
    else:
        print("Ejecución cancelada.")

if __name__ == "__main__":
    main()
