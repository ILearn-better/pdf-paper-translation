from flask import Flask, render_template, request,jsonify,send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("./save_pdf/"+secure_filename(f.filename))

        data = {
            'status': 1,
            'message': 'This is an example API response',
            'data': {
                'example_key': 'example_value'
            }
        }
        return jsonify(data)
    else:
        return render_template('upload.html')

def download():
    filename = 'example.txt'
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

