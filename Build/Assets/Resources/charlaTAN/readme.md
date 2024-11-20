# Charlatan 2022
Charlatan es una extensi�n del framework Rasa desarrollada por un grupo de alumnos durante la cursada de Ingenieria 2022. El objetivo principal es el de albergar multiples agentes en un �nico proceso. Estos agentes pueden ser desarrollados con Rasa o con la extensi�n desarrolada por Charlatan, la cual permmite que el agente determine que accion debe de ejecutar por medio de una regla definida en Prolog. Por �ltimo otra caracter�stica que brinda Charlatan es la de comunicaci�n entre los agentes que viven dentro del sistema.

## Instalacion:
- Rasa 3.0 minimo
- Charlatan 2022
- SWI Prolog
- swiplserver 

## Instrucciones:
#### - Migrar de Rasa a Charlatan: 
- ##### Como a�adir tu Chatbot
Simplemente el proyecto desarrollado con el Framework Rasa debe de arrastrarse hasta la carpeta _**agents**_ definida en Charlatan. El nombre que lleve dicha carpeta determinar� el nombre que recibir� el agente y como uno podr� referirse a �l
- ##### Como usar customs actions
Para utilizar las customs actions debe de definirle a cada uno de sus agentes un endpoint distinto, por lo tanto deber� iniciar un servidor de acciones por cada agente que requiera utilizar

## Uso:
- #### General:
Con la siguiente instruccion pondr� en ejecucion el servidor de Charlatan el cual se encargar� de poner en ejecucion cada uno de los Agents definidos en _**agents/**_  
``` python -m rasa run --enable-api --cors "*" -p 5012 ```
 * Tenga en cuenta que el comando se ejecuta posicionado en la root donde tiene definido Charlatan, es decir `..somepath\charlatan`

- #### Dialogando con Charlatan:
 - Para dialogar con un agente espec�fico deber� de 
``` python -m rasa shell --agent <agent_name> ```

 - Para dialogar por medio de HTTP deber� ejecutar el servidor de Charlatan y luego tiene dos alternativas
    - Query Params: ```http://localhost:5012/webhooks/rest/webhook/?receiver=minorista```
    Tener en cuenta que el Json body deberia: ```{"message": "hola","sender": "mati"```
    - Json Body: ```{"message": "hola","sender": "mati", "metadata": 
    {"agent_name": "minorista"}}``` con la URL ```http://localhost:5012/webhooks/rest/webhook```

- #### Entrenamiento:
Para entrenar el modelo de un agente especifico
``` python -m rasa train --agent <agent_name> ```
- #### Custom actions:
Deber� configurar el endpoints.yml por cada agente que requiera usar las customs actions, debe tener encuenta que deber� ser un enpoint diferente. A su vez tendr� que iniciar un proceso del servidor de actions por cada agente que lo requiera

## Documentacion: 
[Click aqui para ir a la documentacion.](https://drive.google.com/drive/folders/1VXtXtrjIPhMwlzVIrHUsZK1E8M0scZqz?usp=sharing)

Consideracion final: Una vez instalado rasa puede eliminar de la carpeta de su entorno virtual la folder __rasa__ ya que solo se pidio instalar rasa previamente para tener todas las dependencias necesarias

Contacto:
Matias Berthelot (matuberthelot@gmail.com)

Ultima modificacion: 1/10/2022