from flask import Flask, render_template, request, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['GET'])
def execute():
    command = request.args.get('command')
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    def generate():
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                yield f"data: {line}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
