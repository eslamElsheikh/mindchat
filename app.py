# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
# import google.generativeai as genai
# from typing import List
# import os

# app = Flask(__name__)
# load_dotenv()

# THERAPIST_INTRO = """Your name is Dr. Sanchez. You are an expert in psychotherapy, especially DBT.
#                       You hold all the appropriate medical licenses to provide advice.
#                       You have been helping individuals with their stress, depression and anxiety for over 20 years.
#                       From young adults to older people. Your task is now to give the best advice to individuals seeking help managing their symptoms.
#                       You must ALWAYS ask questions BEFORE you answer so that you can better hone in on what the questioner is really trying to ask.
#                       You must treat me as a mental health patient.
#                       Your response format should focus on reflection and asking clarifying questions.
#                       You may interject or ask secondary questions once the initial greetings are done.
#                       Exercise patience."""

# def initialize_model() -> genai.GenerativeModel:
#     genai.configure(api_key="AIzaSyD4lD8pcLQaSaoBiQQMUHRCoOTekeejUlU")
#     return genai.GenerativeModel("gemini-pro")

# def construct_message(message: str, role: str = 'user') -> dict:
#     return {
#         'role': role,
#         'parts': [
#             {'text': message}
#         ]
#     }

# def get_model_response(model: genai.GenerativeModel, conversation: List[dict]) -> dict:
#     response = model.generate_content(conversation)
#     response.resolve()
#     return construct_message(response.text, 'model')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get("message")
#     conversation = request.json.get("conversation", [])
    
#     if not conversation:
#         conversation.append(construct_message(THERAPIST_INTRO))
    
#     conversation.append(construct_message(user_input))
    
#     model = initialize_model()
#     response = get_model_response(model, conversation)
#     conversation.append(response)
    
#     return jsonify(conversation=conversation)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List
import os
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
load_dotenv()

THERAPIST_INTRO = """Your name is Dr. Sanchez. You are an expert in psychotherapy, especially DBT.
                      You hold all the appropriate medical licenses to provide advice.
                      You have been helping individuals with their stress, depression and anxiety for over 20 years.
                      From young adults to older people. Your task is now to give the best advice to individuals seeking help managing their symptoms.
                      You must ALWAYS ask questions BEFORE you answer so that you can better hone in on what the questioner is really trying to ask.
                      You must treat me as a mental health patient.
                      Your response format should focus on reflection and asking clarifying questions.
                      You may interject or ask secondary questions once the initial greetings are done.
                      Exercise patience."""

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    text = db.Column(db.Text, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

def initialize_model() -> genai.GenerativeModel:
    genai.configure(api_key="AIzaSyD4lD8pcLQaSaoBiQQMUHRCoOTekeejUlU")
    return genai.GenerativeModel("gemini-pro")

def construct_message(message: str, role: str = 'user') -> dict:
    return {
        'role': role,
        'parts': [
            {'text': message}
        ]
    }

def get_model_response(model: genai.GenerativeModel, conversation: List[dict]) -> dict:
    response = model.generate_content(conversation)
    response.resolve()
    return construct_message(response.text, 'model')

def save_conversation(conversation_data):
    with app.app_context():
        conversation = Conversation()
        db.session.add(conversation)
        db.session.commit()  # Save conversation to get the ID

        for message_data in conversation_data:
            message = Message(role=message_data['role'], text=message_data['parts'][0]['text'], conversation_id=conversation.id)
            db.session.add(message)
        
        db.session.commit()

def load_conversation(conversation_id):
    with app.app_context():
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return []
        return [
            {
                'role': message.role,
                'parts': [{'text': message.text}]
            }
            for message in conversation.messages
        ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        logging.info("Chat endpoint reached")
        user_input = request.json.get("message")
        conversation_id = request.json.get("conversation_id")
        
        logging.info(f"User input: {user_input}")
        logging.info(f"Conversation ID: {conversation_id}")
        
        if conversation_id:
            conversation = load_conversation(conversation_id)
        else:
            conversation = [construct_message(THERAPIST_INTRO)]
        
        conversation.append(construct_message(user_input))
        
        model = initialize_model()
        response = get_model_response(model, conversation)
        conversation.append(response)
        
        if not conversation_id:
            save_conversation(conversation)
            with app.app_context():
                conversation_id = Conversation.query.order_by(Conversation.id.desc()).first().id
        else:
            save_conversation(conversation)
        
        json_response = jsonify(conversation=conversation, conversation_id=conversation_id)
        logging.info(f"JSON response: {json_response.json}")
        return json_response
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
