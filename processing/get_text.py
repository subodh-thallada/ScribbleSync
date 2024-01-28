from flask import Flask, request, render_template, jsonify
import os
import numpy as np
from functions import *

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(uploads_dir, exist_ok=True)

picture_path = None

@app.route('/')
def page():
    return render_template('page.html')


@app.route('/save_data', methods=['POST'])
def save_data():
    global picture_path
    if request.is_json:
        data = request.json
        text_data = data.get('text')
        if text_data:
            print("This is was returned:", text_data['data'])
            return jsonify({"events":["Meeting 1", "Meeting 2"], 
                "links": ["https://calendar.google.com/calendar/u/0/r", "https://www.google.com"], 
                "notes": ["This is a note", "another note"]})
        else:
            return jsonify({"error": "No text provided"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        # Call your independent processing function
        result = process_data_func()
        return jsonify({"message": "Processing successful", "result":f"{result}"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error occurred during processing"}), 500

def process_data_func():
    global picture_path
    # Pictures
    if picture_path.endswith('.png') or picture_path.endswith('.jpg') or picture_path.endswith('.jpeg'):
        print('load image')
        print('load image clear')
        if not os.path.exists(picture_path):
            print(picture_path)
            print('fuck')
            return jsonify({"error": "File not found"}), 400
        else:
            try:
                print('problem')
                text = handwrite_ocr(picture_path)
                print(text)
                text = text.replace('\n', ' ')
                print('ocr clear')
                json_content = json_create(text)
                print('1st cohere clear')
                json_content = {
                    "notes": ["convert jira adp into markdown", "pull manual tests from jira"],
                    "events": ["meeting at 3PM with Chris today", "submit pull request tomorrow by 2PM"]
                }
                events, time_list = grab_time(json_content)
                print('2nd cohere clear')
                time_list = ["2024-01-27T15:00:00", "2024-01-28T14:00:00"]
                links = make_event(events, time_list)
                print('google calender clear')
                output = {'Meetings':events, "Time":time_list, "Link":links}
            except Exception as e:
                print(e)
                return jsonify({"error": "Error occurred while processing image"}), 500
            return output
    # PDF
    elif picture_path.endswith('.pdf'):
        pdf_path = picture_path
        if not os.path.exists(pdf_path):
            return jsonify({"error": "File not found"}), 400
        else:
            try:
                text = text_ocr(pdf_path)
                json_content = json_create(text)
                events, time_list = grab_time(json_content)
                links = make_event(events, time_list)
                output = {'Meetings':events, "Time":time_list, "Link":links}
            except Exception as e:
                print(e)
                return jsonify({"error": "Error occurred while processing image"}), 500
            return output
    # Simply text
    else:
        text = picture_path
        try:
            json_content = json_create(text)
            events, time_list = grab_time(json_content)
            links = make_event(events, time_list)
            output = {'Meetings':events, "Time":time_list, "Link":links}
        except Exception as e:
            print(e)
            return jsonify({"error": "Error occurred while processing image"}), 500
        return output

if __name__ == '__main__':
    app.run(debug=True)