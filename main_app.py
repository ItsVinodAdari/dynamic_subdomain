from re import sub
from flask import Flask, url_for, Blueprint, render_template, request, redirect
from json import dumps, loads
app = Flask(__name__)
bp = Blueprint('subdomain', __name__, subdomain="<user>")
server_name = 'vinkkk.com'

@app.route('/')
def index():
    user_data = loads(open('./users.json','r').read())
    return render_template('/index.html', users=user_data, host=server_name)

@bp.route('/')
def subdom(user):
    return f"welcome to your subdomain - {user}"

# @app.route('/test')
# def test():
#  return url_for('index', _external=True)

@app.route('/register', methods=['POST'])
def register():
    user_data = loads(open('./users.json','r').read())
    user_name = request.form['name']
    add_subdomain(user_name)
    user_count = len(user_data)
    user_data.update({user_count + 1: user_name})
    json_data = dumps(user_data)
    open('./users.json', 'w').write(json_data)

    return redirect(url_for('index', result_id=user_count))
    # return dumps({'response': True})

def add_subdomain(user):
    host_file = open('/etc/hosts', 'r').read()
    subdomain = f"{user}.{server_name}"
    
    if subdomain not in host_file:
        with open('/etc/hosts', 'w') as write_host:

            append_subdomain = f"{host_file} \n127.0.0.1 {subdomain}"
            write_host.write(append_subdomain)

if __name__ == "__main__":
    app.config['SERVER_NAME'] = f"{server_name}:5000"
    app.register_blueprint(bp)
    app.run(debug=True)