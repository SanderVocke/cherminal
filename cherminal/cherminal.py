from flask import Flask, render_template, request, Response
from flask_httpauth import HTTPBasicAuth
from passlib.apache import HtpasswdFile
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Run a shell process and host a webpage to "chat" with it.')
parser.add_argument('-c', '--command', required=True, help='The command to run as a subprocess.')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode.')
parser.add_argument('--password', help='Path to htpasswd file for basic authentication.')
args = parser.parse_args()

command = args.command
debug_mode = args.debug
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)

auth = HTTPBasicAuth()
password_file = HtpasswdFile(args.password) if args.password else None

@auth.verify_password
def verify_password(username, password):
    if not password_file:
        print("No password file provided. Skipping authentication.")
        return True
    if password_file.check_password(username, password):
        print(f"Authentication successful for user: {username}")
        return username
    print(f"Authentication failed for user: {username}")
    return None

@auth.error_handler
def unauthorized():
    if request.authorization:
        return render_template('unauthorized.html'), 401
    return render_template('unauthorized.html'), 401

import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def exit_server():
    print("Subprocess exited. Shutting down the server.")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()

@app.route('/')
def index():
    if password_file:
        print("Basic authentication enabled.")
        return auth.login_required(lambda: render_template('index.html', command=command, debug_mode=debug_mode))()
    print("Basic authentication not enabled.")
    return render_template('index.html', command=command, debug_mode=debug_mode)


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    global process
    if request.method == 'POST':
        command = request.form.get('command')
        if debug_mode:
            print(f"Input sent: {command}")
        process.stdin.write(command + '\n')
        process.stdin.flush()
        return '', 204
    else:
        def generate():
            while True:
                line = process.stdout.readline()
                if not line:
                    if process.poll() is not None:
                        exit_server()
                    break
                if line:
                    yield f"data: {line}\n\n"
        return Response(generate(), mimetype='text/event-stream')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
