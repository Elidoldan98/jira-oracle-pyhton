# Jira-Oracle-Pyhton
Herramienta para la automatizacion de ejecucion de Tickets, en proyectos como JIRA, en bases de datos ORACLE, con BK automaticos en EXCELL y todo implementado en PYHTON.

Esta herramienta utiliza librerias de pyhton como JIRA, Cx_ORACLE, PANDAS, para la ejecucion de querys SQL en bases de datos y totalmente automatizado, sin tener que realizar una interacion manual. 

La funcion CORE es 

1 Utilizar la API de JIRA para verificar el TICKET en cuestión, que nos da la descripcion del mismo con el query SQL 
2 Verificar el texto con pyhton para buscar sentencias SQL.
3 Ejecutar esas sentencias en la DB en cuestion.
4 Comentar, cambiar estado y adjuntar BK en excell si habia que hacerlas como consultas en el ticket. 




