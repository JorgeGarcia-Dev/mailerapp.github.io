import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

# Crea una conexión a la base de datos si aún no existe, y devuelve la conexión y cursor.
# :return: Una tupla de la conexión a la base de datos y el cursor.
def get_db():
    # Comprobando si la conexión a la base de datos ya está en el objeto `g`.
    if 'db' not in g:
        # Crear una conexión a la base de datos.
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'], 
        )
        # Creación de un objeto de cursor que se utilizará para ejecutar sentencias SQL.
        g.c = g.db.cursor(dictionary=True)
    # Devolviendo la conexión a la base de datos y el cursor..
    return g.db, g.c

# It closes the database connection
# :param e: The exception that was raised, if any
def close_db(e=None):
    
    # Eliminando la clave `db` del objeto `g` si existe.
    db = g.pop('db', None)
    
    # Cierra la conexión a la base de datos.
    if db is not None:
        db.close()
        
# Crea una conexión de base de datos, crea un cursor y ejecuta las instrucciones SQL en el
# lista de `instrucciones`.
def init_db():
    # Está obteniendo la conexión de la base de datos y el cursor.
    db, c = get_db()
    
    # Ejecutando las instrucciones SQL en la lista de `instrucciones`.
    for i in instructions:
        c.execute(i)
        
    # Confirmar los cambios en la base de datos..
    db.commit()

# Crea un nuevo comando de línea de comando llamado init-db que llama a la función init_db y muestra un
# mensaje de exito al usuario.
@click.command('init-db')
# Le dice a Flask que llame a esa función cuando limpie después de devolver la respuesta.
@with_appcontext
# Crea una tabla de base de datos llamada entradas, que tiene dos columnas: título y texto
def init_db_command():
    # Crear una conexión de base de datos, crear un cursor y ejecutar las instrucciones SQL en la lista
    # de `instrucciones`.
    init_db()
    # Imprimiendo un mensaje al terminal.
    click.echo("Base de datos inicializada")

# Le dice a Flask que llame a esa función cuando limpie después de devolver la respuesta
# :param app: La instancia de la aplicación Flask.  
def init_app(app):
    # Le dice a Flask que llame a esa función cuando limpie después de devolver la respuesta.
    app.teardown_appcontext(close_db)
    # Agrega un nuevo comando que se puede llamar con el comando matraz.
    app.cli.add_command(init_db_command)