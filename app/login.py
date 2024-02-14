from flask import jsonify, Blueprint, request, render_template, redirect, json, session, url_for
import os
import random
from user_agents import parse
from app.privileges import loged_user

bp = Blueprint('login_blueprint', __name__,  url_prefix="/")
# Función para cargar los usuarios desde un archivo JSON
def load_users():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(dir_path, 'static', 'users', 'users.json')

    with open (json_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

@bp.route('/', methods=['GET', 'POST'])
def index():
     return redirect(url_for('login_blueprint.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
     session.clear()
     user_agent = request.headers.get('User-Agent')
     ua = parse(user_agent)
     browser = ua.browser.family
     version = ua.browser.version_string
     ip_addr = request.remote_addr

     session['user_agent'] = str(ua)
     session['browser'] = browser
     session['version'] = version
     session['ip_addr'] = ip_addr
     error = None
     if request.method == 'POST':
          username = request.form['username']
          users = load_users()['users']
          user_exists = any(user['nickname'] == username for user in users)
          if username == '':
               return redirect(url_for('login_blueprint.login'))
          if user_exists:               
               user = next((user for user in users if user['nickname'] == username), None)
               if user:
                    validation_ip = 'IP no registrada'
                    validation_b = 'Navegador No registrado'
                    found_match = False
                    found_ip = False
                    for browser_id, browser_info in user['browsers'].items():
                         if browser_info['type'] == browser:
                              validation_b = ''
                              found_match = True
                         else:
                              found_match

                         if browser_info['ip'] == ip_addr:
                                   validation_ip = ''
                                   found_ip = True
                         else: 
                                   found_ip
                    if found_ip and found_match:
                         session['username'] = username
                         return redirect(url_for('login_blueprint.recognition', 
                                       validation_ip = validation_ip, validation_b=validation_b))
                    else: return redirect(url_for('verificate_blueprint.verificate',
                                                      validation_ip = validation_ip, validation_b=validation_b)) 
               
               
               if validation_ip  == '' or validation_b == '':
                    return redirect(url_for('login_blueprint.recognition', 
                                       validation_ip = validation_ip, validation_b=validation_b))
               else: return redirect(url_for('login_blueprint.recognition'))
          else:
               error = 'Usuario no encontrado'

     return render_template('index.html', error=error)

@bp.route('/recognition', methods=['GET', 'POST'])
@loged_user
def recognition():

    # Obteniendo la ruta absoluta del directorio actual
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(dir_path, 'static', 'phrases', 'phrases.json')
    with open (json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        phrases_list = list(data['recognize-phrases'].values())
        selected_phrases_list = random.sample(phrases_list, 3)
        selected_phrases = {str(i): phrase for i, phrase in enumerate(selected_phrases_list)}
        validation_ip = request.args.get('validation_ip', 'Reconociendo IP')
        validation_b = request.args.get('validation_b', 'Reconociendo Navegador Web')
        return render_template('form-recognition.html', 
                               selected_phrases=selected_phrases)

@bp.route('/register', methods=['GET','POST'])
def register():
     if request.method == 'POST':
          try:
               dir_path = os.path.dirname(os.path.realpath(__file__))
               json_path = os.path.join(dir_path, 'static', 'users', 'users.json')

               with open (json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
          except (FileNotFoundError, json.JSONDecodeError):
               data = {'users': []}
          if request.form['name'] or request.form['nickname'] or request.form['email'] or request.form['email']: 
               name = request.form['name']
               nickname = request.form['nickname']
               email = request.form['email'] 
               # Añade el nuevo usuario
               new_user = {
               "id": len(data['users']),
               "name": name,
               "nickname": nickname,
               "email": email,
               "browsers": {
                    
               }
               }
               data['users'].append(new_user)

               # Obteniendo la ruta absoluta del directorio actual
               dir_path = os.path.dirname(os.path.realpath(__file__))
               json_path = os.path.join(dir_path, 'static', 'users', 'users.json')

               # Guarda los cambios en 'users.json'
               with open(json_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
               return redirect(url_for('verificate_blueprint.verificate', email = email))
     else:
          return redirect(url_for('login_blueprint.login'))

@bp.route('/getdata', methods=['POST'])
@loged_user
def getdata():
     username = session.get('username')
     data = request.get_json()
     filename = 'data.json'

     try:
          if os.path.isfile(filename):
               with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
     except (FileNotFoundError, json.JSONDecodeError):
          existing_data = {'data': []}
     if existing_data['data']:
          existing_data['data'].append(data['data'])

     with open(filename, 'w', encoding='utf-8') as f:
          json.dump(existing_data, f, indent=4)

     return jsonify({'message': 'ok'}), 200


@bp.route('/session', methods=['GET'])
def get_session():
    return jsonify(session)
