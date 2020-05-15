from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        return 'Successfully Completed'
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
