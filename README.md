![pyhton](https://github.com/user-attachments/assets/a102967a-27ea-4f5e-8eff-f8752c07150e) 
# **Jira-SQL-Python** 
Automatización de la ejecución de tickets en JIRA, bases de datos Oracle y generación de backups en Excel, todo implementado con Python.

---

## **Descripción**  
Esta herramienta permite automatizar tareas comunes en proyectos que utilizan JIRA y bases de datos Oracle. Gracias a su implementación en Python, simplifica procesos como la ejecución de queries SQL y la generación automática de backups en formato Excel, eliminando la necesidad de interacción manual.

### **Librerías utilizadas**  
- **JIRA**: Para interactuar con la API de JIRA.  
- **cx_Oracle**: Para ejecutar queries en bases de datos Oracle.  
- **Pandas**: Para manipulación de datos y creación de backups en Excel.  

⚠️ **Nota importante:**  
Se requiere cierto conocimiento previo para utilizar este código:  
- Ejecución de código en Python.  
- Manejo de entornos virtuales.  
- Instalación de dependencias.  
- Solución de errores comunes.

---

## **Funcionamiento principal**  

1. **Consulta de tickets en JIRA**:  
   La herramienta utiliza la API de JIRA para verificar la descripción del ticket y extraer las sentencias SQL que contiene.  

2. **Identificación de sentencias SQL**:  
   Utiliza Python para buscar y analizar sentencias SQL en el texto del ticket.  

3. **Ejecución automatizada en la base de datos**:  
   Ejecuta las sentencias en la base de datos correspondiente.  

4. **Gestión del ticket**:  
   Cambia el estado, comenta el ticket, y adjunta backups generados en Excel si es necesario.

---

## **Flujo de trabajo**  

1. Ejecuta el archivo `main.py`.  
2. Ingresa el número del **FSOP** del proyecto (por ejemplo, los últimos 5 dígitos de un enlace de JIRA).  
3. El programa verifica el ticket, extrae y ejecuta las sentencias SQL, y gestiona los backups.

### **Ejemplo visual**  

#### **1. Ingreso del número de FSOP**  
El programa solicita el número de proyecto y procede con la validación:  
![Paso 1](https://github.com/user-attachments/assets/9b8cdcda-6c2b-48fe-bdbb-139cbe776e3b)  

#### **2. Verificación del ticket**  
Muestra detalles del ticket: asignado, estado, y tipo de query detectada.  
![Paso 2](https://github.com/user-attachments/assets/5d2b8aac-1f91-454d-b4aa-1350f8d207c9)  

#### **3. Ejecución de la query**  
En caso de error (por ejemplo, tabla inexistente), el flujo de trabajo continúa:  
![Paso 3](https://github.com/user-attachments/assets/dc7819e7-197f-42bd-b015-15754fd26915)  

#### **4. Generación de backups**  
Las consultas `SELECT` se guardan automáticamente en un archivo Excel y se adjuntan al ticket como respaldo:  
![Backup generado](https://github.com/user-attachments/assets/28ef865e-c5e2-4adb-bf1a-2c4c4c8fa772)  
![foto1](https://github.com/user-attachments/assets/767d0b32-90c7-42ae-8fe7-21656d5c960b)


---

## **Consideraciones finales**  
- Esta es la **versión inicial** de la herramienta. Pueden presentarse errores, por lo que siempre es recomendable verificar las sentencias SQL antes de ejecutarlas.  
- La herramienta se encuentra en desarrollo y se aceptan sugerencias para mejorar su funcionalidad.

---

## **Contacto**  
Si tienes dudas, sugerencias o encuentras errores, no dudes en contactarme:  
📧 **Correo**: Eliasdoldan7@gmail.com  
🌐 **LinkedIn**: [Elias Doldan Valdez](https://www.linkedin.com/in/elias-doldan-valdez-1b360b167/)












