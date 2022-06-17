import os

from flask import Flask

# Crea una aplicación Flask, carga la configuración de las variables de entorno, inicializa el
# base de datos y registra el modelo de correo.
# :return: El objeto de la aplicación está siendo devuelto.
def create_app():
    
    # Creación de un objeto de Aplicación Flask.
    app = Flask(__name__)
    
    # Cargando las variables de entorno en el diccionario app.config.
    app.config.from_mapping(
        FROM_EMAIL=os.environ.get('FROM_EMAIL'),
        SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )
    
    # Importación de la variable db desde el módulo db.
    from . import db
    
    # Inizializa la Base de Datos.
    db.init_app(app)
    
    # Importa el blueprint desde el módulo de correo.
    from . import mail
    
    # Registra el blueprint de el módulo de correo.
    app.register_blueprint(mail.bp)
    
    
    # Devuelve el objeto de la aplicación.
    return app