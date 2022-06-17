from flask import (
    Blueprint, redirect, render_template, request, flash, url_for, current_app
)

import sendgrid
from sendgrid.helpers.mail import *

from app.db import get_db

# Creando un proyecto llamado `correo` con el prefijo `/`.
bp = Blueprint('mail', __name__, url_prefix="/")

# Un decorador que le dice a Flask qué URL debe activar nuestra función.
@bp.route('/', methods=['GET'])
# Obtiene el parámetro de búsqueda de la URL, luego obtiene todos los correos electrónicos de la base de datos u
# obtiene los correos electrónicos que contienen la cadena de búsqueda.
def index():
    # El objeto `request.args` almacena todos los datos que se envían con la URL.
    search = request.args.get('search')
    # `get_db()` devuelve una conexión a la base de datos y un cursor.
    db, c = get_db()
    # Si el parámetro de búsqueda no está presente en la URL, la consulta devolverá todos los correos electrónicos.
    if search is None:
        c.execute("SELECT * FROM email")
    # Si no se cumplio la anterior condición, se ejecuta else y devuelve todos los registros de la base de datos.
    else:
        c.execute("SELECT * FROM email WHERE content like %s", ('%' + search + '%',))
    # `c.fetchall()` devuelve una lista de todas las filas de la tabla.
    mails = c.fetchall()
    
    # Imprime los correos.
    print(mails)
    # Retorna la plantilla de 'index.html'    
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])

#Si el método de solicitud es POST, obtenga el correo electrónico, el asunto y el contenido del formulario, compruebe si están
# vacío, y si no lo están, envíe el correo electrónico y guárdelo en la base de datos
# :return: la plantilla 'mails/create.html'
def create():
    # Comprobando si el método de solicitud es POST.
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []
        
        # Comprueba si el campo de correo electrónico está vacío y, si lo está, agrega un error a la lista de errores.
        if not email:
            errors.append('Email es obligatorio')
        # Comprueba si el campo de asunto está vacío y, si lo está, agrega un error a la lista de errores.
        if not subject:
            errors.append('Asunto es obligatorio')
        # Comprueba si el campo de contenido está vacío y, si lo está, agrega un error a la lista de errores.
        if not content:
            errors.append('Contenido es obligatorio')
            
        # Si no hay errores, la función envía el correo electrónico, lo guarda en la base de datos y
        # redirige al usuario a la página de índice.
        if len(errors) == 0:
            send(email, subject, content)
            # `get_db()` devuelve una conexión a la base de datos y un cursor.
            db, c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
            # `db.commit()` guarda los cambios en la base de Datos.
            db.commit()
            # `url_for()` es una función que genera direcciones URL para un punto final dado.
            return redirect(url_for('mail.index'))
        # Si no se cumple ninguna de las anteriores condiciones, else recorre los errores y envía un mensaje flash con el error.
        else:
            for error in errors:
                flash(error)
    # Retorna la plantilla 'create.html'   
    return render_template('mails/create.html')

# Envía un correo electrónico a la dirección especificada con el asunto y el contenido especificados.
# :param to: La dirección de correo electrónico del destinatario.
# :param subject: El asunto del correo electrónico.
# :param content: El contenido del correo electrónico.
def send(to, subject, content):
    # Crea un cliente SendGrid con la clave API especificada en la variable de configuración `SENDGRID_KEY`.
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    # `from_email` es un objeto que representa al remitente del correo electrónico.
    from_email = Email(current_app.config['FROM_EMAIL'])
    # `To()` es una clase que crea un objeto que representa al destinatario del correo electrónico.
    to_email = To(to)
    # `Content()` es una clase que crea un objeto que representa el contenido del correo electrónico.
    content = Content('text_plain', content)
    # Crea un objeto que representa el correo electrónico..
    mail = Mail(from_email, to_email, subject, content)
    # Envía el correo electrónico.
    response = sg.client.mail.send.post(request_body=mail.get())
    # Imprime la respuesta.
    print(response)
    