![pyhton](https://github.com/user-attachments/assets/a102967a-27ea-4f5e-8eff-f8752c07150e) 
# **Jira-SQL-Python**  
Automatización de tickets en JIRA, ejecución de SQL en Oracle y generación de backups en Excel, todo con Python.

---

## **Descripción**  
Esta herramienta permite automatizar tareas comunes en proyectos que utilizan JIRA y bases de datos Oracle. Simplifica procesos como la ejecución de consultas SQL y la generación automática de backups en Excel, eliminando la necesidad de interacción manual.

### **Librerías utilizadas**  
- **JIRA**: Para interactuar con la API de JIRA.  
- **cx_Oracle**: Para ejecutar queries en bases de datos Oracle.  
- **Pandas**: Para manipulación de datos y creación de backups en Excel.  

> ⚠️ **Nota importante:**  
> Se requiere conocimiento previo de Python: ejecución de código, manejo de entornos virtuales, instalación de dependencias y solución de errores.

---

## **Funcionamiento principal**  

1. **Consulta de tickets en JIRA**  
   Verifica la descripción del ticket y extrae las sentencias SQL.  

2. **Identificación de sentencias SQL**  
   Analiza el texto del ticket para localizar queries SQL.  

3. **Ejecución automatizada en la base de datos**  
   Ejecuta las sentencias SQL en la base de datos correspondiente.  

4. **Gestión del ticket**  
   Cambia el estado, comenta el ticket, y adjunta backups generados en Excel.

---

## **Flujo de trabajo**  

1. Ejecuta el archivo `main.py`.  
2. Ingresa el número del **FSOP** (últimos 5 dígitos de un enlace de JIRA).  
3. El programa verifica el ticket, extrae y ejecuta las sentencias SQL, y gestiona los backups.

---

## **Ejemplo visual**  

### **1. Ingreso del número de FSOP**  
El programa solicita el número del proyecto y procede con la validación:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/9b8cdcda-6c2b-48fe-bdbb-139cbe776e3b" alt="Paso 1" width="70%">  
</p>  

### **2. Verificación del ticket**  
Muestra detalles del ticket: asignado, estado, y tipo de query detectada:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/5d2b8aac-1f91-454d-b4aa-1350f8d207c9" alt="Paso 2" width="70%">  
</p>  

### **3. Ejecución de la query**  
Si ocurre un error (por ejemplo, tabla inexistente), el flujo de trabajo continúa:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/dc7819e7-197f-42bd-b015-15754fd26915" alt="Paso 3" width="70%">  
</p>  

### **4. Generación de backups**  
Las consultas `SELECT` se guardan automáticamente en un archivo Excel y se adjuntan al ticket como respaldo:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/28ef865e-c5e2-4adb-bf1a-2c4c4c8fa772" alt="Backup generado" width="70%">  
</p>  

### **5. Ejecución completa con queries de modificación**  
Ingresamos el ticket y el programa ejecuta las sentencias SQL correctamente:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/845ca0d7-05ac-48db-9cc0-7458bf4bf403" alt="Ingreso del ticket" width="70%">  
</p>  

El programa realiza los comentarios y adjuntos en el ticket de JIRA:  
<p align="center">  
  <img src="https://github.com/user-attachments/assets/747ba11e-b18a-4d18-b9fd-d1428c556a9e" alt="Ejecución completada" width="70%">  
</p>  

---

## **Consideraciones finales**  
- **Versión inicial**: Pueden presentarse errores. Verifica siempre las sentencias SQL antes de ejecutarlas.  
- Se aceptan sugerencias para mejorar la herramienta.  

---

## **Advertencia**  

⚠️ **IMPORTANTE** ⚠️  
- Este código no debe utilizarse con fines de lucro.  
- Uso exclusivo para aprendizaje o propósitos personales.  

---

## **Contacto**  
📧 **Correo**: Eliasdoldan7@gmail.com  
🌐 **LinkedIn**: [Elias Doldan Valdez](https://www.linkedin.com/in/elias-doldan-valdez-1b360b167/)









