from datetime import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time
from flask import json, Blueprint, request, session
from app import login as lu

bp = Blueprint('sd', __name__,  url_prefix="/")

def generate_random_code():
    # Obtén el tiempo actual en segundos
    current_time = int(time.time())
    # Si el tiempo actual tiene menos de 6 dígitos, rellena con ceros a la izquierda
    code = str(current_time).zfill(6)[-6:]
    
    return code

@bp.route('/send_message', methods=['POST'])
def send_message():
    email = request.form['email']
    print(email)
    code = generate_random_code()
    
    message = Mail(
        to_emails=email,
        from_email='xxxxxxxxxxxxxxxxxx',
        subject='Por favor verifica tu cuenta',
        html_content=f'<p>Tu codigo de verificacion es: <strong> {code} </strong></p>')
    try:
        sendgrid_client = SendGridAPIClient('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        response = sendgrid_client.send(message)
        change_state(email, 'blocked', code)

    except Exception as e:
        print(e.args[0])

    return 'ok'

def change_state(email, state, code):
    users_data = lu.load_users()
    users = users_data['users']
    user = next((user for user in users if user['email'] == email), None)
    if user:
    # Agregar el estado y el código al usuario
        user['state'] = {
        "state":state,
        "code": code
    }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(dir_path, 'static', 'users', 'users.json')  

        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)
    return 'ok'

def add_browser(email):
    user_agent = session.get('user_agent', '')
    browser = session.get('browser', '')
    version = session.get('version', '')
    ip_addr = session.get('ip_addr')
    users_data = lu.load_users()
    users = users_data['users']
    user = next((user for user in users if user['email'] == email), None)
    if user:
        # Generar un ID único para el nuevo navegador
        new_browser_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(len(user['browsers']))
        new_browser = {
            new_browser_id:{
            "User Agent": user_agent,
            "type": browser,
            "version": version,
            'ip': ip_addr
            }}
        # Agregar el nuevo navegador al diccionario de navegadores del usuario
        user['browsers'].update(new_browser)
    
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(dir_path, 'static', 'users', 'users.json') 
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)
    return 'ok'