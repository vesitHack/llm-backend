# Storytelling Companion Backend

A FastAPI backend service that powers the Storytelling Companion application using Google's Gemini AI model.

## Features

- Story idea generation
- Plot development assistance
- Character creation
- Dialogue generation
- Text analysis and feedback

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# OR
venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /generate-story-ideas` - Generate story ideas based on premise, genre, and themes
- `POST /develop-plot` - Create plot outlines with three-act structure
- `POST /create-character` - Generate detailed character profiles
- `POST /generate-dialogue` - Create natural dialogue for characters
- `POST /analyze-text` - Analyze writing and provide feedback

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (required)

## Development

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
