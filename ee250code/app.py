from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    output = subprocess.check_output(["python", "grovepicode.py"]).decode("utf-8")

    return render_template('index.html', title='TV Shows on Selected Date', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
