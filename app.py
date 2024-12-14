from flask import Flask, render_template, request, Response
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python app.py <command>")
    sys.exit(1)

command = sys.argv[1]
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)

app = Flask(__name__)

def exit_server():
    print("Subprocess exited. Shutting down the server.")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    global process
    if request.method == 'POST':
        command = request.form.get('command')
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
