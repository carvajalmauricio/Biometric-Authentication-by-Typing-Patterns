from flask import Blueprint, request, render_template, redirect, json, session, url_for
from app.send_message import change_state, add_browser
from app.login import load_users

bp = Blueprint('verificate_blueprint', __name__,  url_prefix="/")

@bp.route('/verificate', methods=['POST', 'GET'])
def verificate():
    validation_ip = request.args.get('validation_ip', '')
    validation_b = request.args.get('validation_b', '')
    if request.method == 'POST':
        error = None
        email = request.form['email']
        if request.form['code']:
            code = request.form['code']
            users_data = load_users()
            # Buscar al usuario por correo electrónico y extraer el valor de state.state
            matching_users = [user for user in users_data['users'] if user.get('email') == email]
            if matching_users:
                user_state = matching_users[0]['state']['state']
                user_code = matching_users[0]['state']['code']
                user_nickname = matching_users[0]['nickname']
                if user_state == 'blocked':
                    if code == user_code:
                        change_state(email, 'unlocked', '')
                        add_browser(email)
                        session['username'] = user_nickname
                        return redirect(url_for('login_blueprint.recognition'))
                    else:
                        error = 'Codigo incorrecto, por favor intente nuevamente'
                        return render_template('verificate_account.html', error=error)
                else:
                    # Retornar un mensaje de error si el estado no es 'blocked'
                    return f"""<a href="{url_for('login_blueprint.login')}">Su usuario ya ha sido desbloqueado Dirijase al inicio</a>""", 400
               
            else:
                return f"""<a href="{ url_for('login_blueprint.register')}">Intente nuevamente</a>""", 404
        else:
            return f"""<a href="{ url_for('login_blueprint.register')}">Intente nuevamente</a>""", 404

    elif request.method == 'GET':
        return render_template('verificate_account.html', validation_ip=validation_ip, validation_b=validation_b)
    


        
