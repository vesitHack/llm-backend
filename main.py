from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Storytelling Companion API")
genai.configure(api_key='AIzaSyD48JR8KHY9HoO_NGSVjo5lfDRT8kfrQ6o')
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Add an OPTIONS route handler for preflight requests
@app.options("/{path:path}")
async def options_handler(request: Request):
    return {}

class StoryIdea(BaseModel):
    premise: str
    genre: Optional[str] = None
    themes: Optional[List[str]] = None

class Character(BaseModel):
    name: str
    description: Optional[str] = None
    traits: Optional[List[str]] = None
    backstory: Optional[str] = None

class DialogueRequest(BaseModel):
    character_name: str
    context: str
    personality: Optional[str] = None

class PlotDevelopment(BaseModel):
    story_premise: str
    current_point: Optional[str] = None
    desired_outcome: Optional[str] = None

@app.post("/generate-story-ideas")
async def generate_story_ideas(idea: StoryIdea):
    try:
        prompt = f"Generate 3 unique story ideas based on the premise: '{idea.premise}'"
        if idea.genre:
            prompt += f" in the {idea.genre} genre"
        if idea.themes:
            prompt += f" incorporating themes of {', '.join(idea.themes)}"
        
        response = model.generate_content(
            [
                "You are a creative writing assistant specializing in story development.",
                prompt
            ]
        )
        return {"ideas": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/develop-plot")
async def develop_plot(plot: PlotDevelopment):
    try:
        prompt = (
            f"Create a detailed plot outline for a story with the premise: '{plot.story_premise}'\n"
            f"Current point in story: {plot.current_point if plot.current_point else 'beginning'}\n"
            f"Desired outcome: {plot.desired_outcome if plot.desired_outcome else 'open'}\n"
            "Include: Three-act structure, major plot points, and potential conflicts."
        )
        
        response = model.generate_content(
            [
                "You are a story structure expert helping to develop compelling plots.",
                prompt
            ]
        )
        return {"plot_outline": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-character")
async def create_character(character: Character):
    try:
        prompt = f"Create a detailed character profile for {character.name}"
        if character.description:
            prompt += f" who is {character.description}"
        if character.traits:
            prompt += f" with the following traits: {', '.join(character.traits)}"
        if character.backstory:
            prompt += f". Consider this backstory: {character.backstory}"
        
        response = model.generate_content(
            [
                "You are a character development expert helping to create deep, realistic characters.",
                prompt
            ]
        )
        return {"character_profile": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-dialogue")
async def generate_dialogue(dialogue: DialogueRequest):
    try:
        prompt = (
            f"Generate natural dialogue for a character named {dialogue.character_name} "
            f"in the following context: {dialogue.context}"
        )
        if dialogue.personality:
            prompt += f"\nThe character's personality is: {dialogue.personality}"
        
        response = model.generate_content(
            [
                "You are a dialogue writing expert specializing in creating natural, character-driven conversations.",
                prompt
            ]
        )
        return {"dialogue": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-text")
async def analyze_text(text: str):
    try:
        prompt = (
            f"Analyze the following text and provide feedback on:\n"
            f"1. Writing style and tone\n"
            f"2. Pacing and flow\n"
            f"3. Character consistency\n"
            f"4. Suggested improvements\n\n"
            f"Text: {text}"
        )
        
        response = model.generate_content(
            [
                "You are a professional editor providing constructive feedback on writing.",
                prompt
            ]
        )
        return {"analysis": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)