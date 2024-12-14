from flask import Flask, render_template, request, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

process = None

@app.route('/execute', methods=['POST'])
def execute():
    global process
    command = request.form.get('command')
    if process is None or process.poll() is not None:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)
        def generate():
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    yield f"data: {line}\n\n"
        return Response(generate(), mimetype='text/event-stream')
    else:
        process.stdin.write(command + '\n')
        process.stdin.flush()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
