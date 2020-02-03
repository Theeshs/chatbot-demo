from flask import Flask, request, make_response, jsonify
import json
import firebase_admin
from firebase_admin import credentials
from flask_cors import CORS
import dialogflow
from google.api_core.exceptions import InvalidArgument
import os

# initialize the app and CORS activating
app = Flask(__name__)
CORS(app)

GOOGLE_APPLICATION_CREDENTIALS = '/home/villvay/PycharmProjects/prodoscore-chat/cred/prodoscore-chat-e4b50c3d7ced.json'


# the route that receive the users' messages
@app.route('/send_message', methods=["POST"])
def access_dialog_flow():
    request_json = request.get_json()
    message = request_json.get('message')
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    print('project id: ', project_id)
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}

    return jsonify(response_text)


# web hook route which is connected with the dialog flow
@app.route('/webhook', methods=['POST'])
def web_hook():
    req = request.get_json(silent=True, force=True)
    res = process_request(req)
    print(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# response processing
def process_request(req):
    query_response = req['queryResult']
    print(query_response)
    text = query_response.get('queryText', None)
    parameters = query_response.get('parameters', None)
    res = get_data()
    return res


# a customized response from the backend
def get_data():
    speech = 'this is from the flask backend'
    return {
        "fulfillmentText": speech
    }


# sending users message to particular user
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    # session_client.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


if __name__ == '__main__':
    app.run()
