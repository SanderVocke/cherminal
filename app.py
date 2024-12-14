from flask import Flask, render_template, request, Response
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description='Run a subprocess and handle input/output.')
parser.add_argument('-c', '--command', required=True, help='The command to run as a subprocess.')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode.')
args = parser.parse_args()

command = args.command
debug_mode = args.debug
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)

app = Flask(__name__)

def exit_server():
    print("Subprocess exited. Shutting down the server.")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()

@app.route('/')
def index():
    return render_template('index.html', command=command)


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

if __name__ == '__main__':
    app.run(debug=True)
