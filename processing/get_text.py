from flask import Flask, request, render_template, jsonify
import os
import numpy as np


app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/')
def page():
    return render_template('page.html')


@app.route('/save_data', methods=['POST'])
def save_data():
    if request.is_json:
        data = request.json
        text_data = data.get('text')
        if text_data:
            print("This is was returned:", text_data['data'])
            return jsonify({"message": "Text received successfully!"})
        else:
            return jsonify({"error": "No text provided"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)