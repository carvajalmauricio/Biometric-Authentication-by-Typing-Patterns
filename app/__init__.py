from flask import Flask, json
from . import login
from datetime import datetime
from . import verificate_user
from . import send_message
from . import privileges
from . import model_preprocessing
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.secret_key = 'noneonekmvufbvjdfcdjcnfjvn'

app.register_blueprint(login.bp)
app.register_blueprint(verificate_user.bp)
app.register_blueprint(send_message.bp)
app.register_blueprint(model_preprocessing.bp)

@app.context_processor
def date_now():
    return {'now': datetime.utcnow()}
