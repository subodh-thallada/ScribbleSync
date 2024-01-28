import requests
import json
import re
from google.cloud import vision
import io
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
import cohere
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

IMAGE_PATH = 'test.jpeg'
PDF_PATH = '/Users/wallacelee/Downloads/BME281L-4th.pdf'
SERVICE_ACCOUNT_FILE = './primal-result-412505-f1d04cf5ff45.json'
CALENDAR_ID = 'miranda.chen2004@gmail.com'

client = vision.ImageAnnotatorClient()
co = cohere.Client('Nvm515TZTewfVajVKjTIqwHWpBjyJpWcI5b8DTXF')


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/calendar']
)
service = build('calendar', 'v3', credentials=credentials)

# ==================== Handwriting OCR ==================== #
def handwrite_ocr(image_path):
    # Load the image into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Call the Vision API
    response = client.document_text_detection(image=image)

    # Display detected text
    for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))
    else:
        return response.full_text_annotation.text

# ==================== PDF OCR ==================== #
def pdf_to_image(pdf_path):
    return convert_from_path(pdf_path, 500)

def text_ocr_wrapper(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))

    return texts

def text_ocr_v2(pdf_path):
    pdf_images = pdf_to_image(pdf_path)
    print('here')
    pages = []
    for image in pdf_images:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Perform OCR using Vision API
        texts = text_ocr_wrapper(img_byte_arr)
        for text in texts:
            print(text.description)
        pages.append(texts.description)

    return pages
    
def text_ocr(pdf_path):
    text = extract_text(pdf_path)
    return text


# ==================== NLP ==================== #
def json_create(text):
    prompt = f"Please classify following content into 2 categories notes, and events: {text}. If it has a time or deadline, it is an event. Also generate the output in just json format with the format of category:list of their items."
    temperature = 0.5

    response = co.generate(
        model='c0051a81-e115-43cb-ba79-41611666f5cb-ft',    # Finetuned model 1 for extracting notes and events
        prompt=prompt,
        temperature=temperature,
    )

    # Extract json content from response
    pattern = r"```json\s+(.+?)\s+```"

    full_content = response.generations[0].text
    match = re.search(pattern, full_content, re.DOTALL)

    if match:
        json_content = match.group(1)
        print(json_content)
        return json_content
    else:
        print(type(full_content))
        print("No JSON content found")
        return None

def convert_time_type(time_json):
    time_list = []
    time_dict = json.loads(time_json)

    for time in time_dict.values():
        if isinstance(time, str):
            datetime_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").isoformat()
        elif isinstance(time, int):
            datetime_obj = (datetime.fromtimestamp(time)).isoformat()
        time_list.append(datetime_obj)
    return time_list

def grab_time(json_content):
    events = json_content['events']
    prompt = f"""
        Please collect the start time of both event in integer after current time {datetime.utcnow()} and put it in a json, beware that there are key works like tomorrow or week after that would affect the number: {events}
    """
    temperature = 0.1
    max_token = 200

    response = co.generate(
        model="2bce82c2-7a18-4fcb-a6b3-dca56d4632c2-ft",    # Finetuned model 2 for extracting time
        prompt=prompt,
        temperature=temperature,
        # max_tokens=max_token,
    )

    # extract list from response
    pattern = r"```json\s+(.+?)\s+```"

    full_content = response.generations[0].text
    match = re.search(pattern, full_content, re.DOTALL)
    print(full_content)
    
    if match:
        time_list = match.group(1)
        print(time_list)
        time_list = convert_time_type(time_list)
        return events, time_list
    else:
        print(type(full_content))
        print("No content found")
        return None

# Debug Testing
# json_create("convert jira adp into markdown, pull manual tests from jira, meeting at 3pm with Chris, submit pull request tomorrow by 2pm")
# json_example = {
#   "notes": ["convert jira adp into markdown", "pull manual tests from jira"],
#   "events": ["meeting at 3PM with Chris today", "submit pull request tomorrow by 2PM"]
# }
# grab_time(json_example)    

# ==================== Google Calendar ==================== #

def make_event(events, time_list):
    links = []
    for i, event in enumerate (events):
        time_couple = time_list[i]
        print(time_couple)
        google_event = {
            'summary': f'{event}',
            'location': '',
            'description': '',
            'start': {
                'dateTime': time_list[i],
                'timeZone': 'EST',
            },
            'end': {
                'dateTime': (datetime.fromisoformat(time_list[i]) + timedelta(hours=1)).isoformat(),
                'timeZone': 'EST',
            },
        }

        # Insert the event
        google_event = service.events().insert(calendarId=CALENDAR_ID, body=google_event).execute()

        print('Event created: %s' % (google_event.get('htmlLink')))
        links.append(google_event.get('htmlLink'))
    return links


# Debug Testing
# make_event(["meeting at 3PM with Chris today", "submit pull request tomorrow by 2PM"], ["2024-01-27T15:00:00", "2024-01-28T14:00:00"])