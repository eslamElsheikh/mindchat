# MindChat

MindChat is an AI-powered virtual therapy assistant that simulates conversations with Dr. Sanchez, an expert in psychotherapy. This project aims to provide accessible mental health support through natural language interactions, with a mobile-first approach.

## Features

- Conversational AI using Google's Generative AI model
- Persistent conversation storage
- Cross-platform mobile app interface
- Therapist persona specializing in stress, depression, and anxiety

## Technology Stack

- Backend: Python 3.x with Flask
- Database: SQLite with SQLAlchemy ORM
- AI Model: Google Generative AI (Gemini Pro)
- Frontend: Flutter for cross-platform mobile development

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Flutter SDK
- Dart SDK
- Google Cloud account with Generative AI API access
- Android Studio or Xcode (for mobile deployment)

## Installation

### Backend Setup

1. Clone the repository:
git clone https://github.com/yourusername/mindchat.git
cd mindchat/backend
Copy
2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
Copy
3. Install the required packages:
pip install -r requirements.txt
Copy
4. Set up environment variables:
Create a `.env` file in the backend directory and add your Google AI API key:
GOOGLE_AI_API_KEY=your_api_key_here
Copy
### Frontend Setup

1. Navigate to the frontend directory:
cd ../frontend
Copy
2. Get Flutter dependencies:
flutter pub get
Copy
## Configuration

- Update the `SQLALCHEMY_DATABASE_URI` in `backend/app.py` if you want to use a different database.
- Modify the `THERAPIST_INTRO` constant in `backend/app.py` to change the AI therapist's persona.
- Update the API endpoint in the Flutter app to point to your backend server.

## Running the Application

### Backend

1. Initialize the database:
python



from app import app, db
with app.app_context():
...     db.create_all()
exit()



Copy
2. Start the Flask server:
python app.py
Copy
### Frontend

1. Ensure you have an Android or iOS emulator running, or a physical device connected.

2. Run the Flutter app:
flutter run
Copy
## Usage

- Launch the MindChat app on your mobile device or emulator.
- Start a new conversation by tapping the new chat button.
- Continue existing conversations by selecting from the conversation list.
- Interact with Dr. Sanchez by typing your messages and receiving AI-generated responses.

## Security Notice

This application deals with potentially sensitive mental health information. Ensure proper security measures are implemented before deploying in a production environment.

## Contributing

Contributions to MindChat are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

MindChat is an AI-based application and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
This README now reflects a project structure with a Flask backend and a Flutter frontend for mobile app development. It includes setup instructions for both t
