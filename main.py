from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
import asyncio
import os
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_key = os.getenv("GROQ_API_KEY")
# print(api_key) 
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = Groq(api_key=api_key)
class PromptRequest(BaseModel):
    concept: str
    level:str

@app.post("/generate")
async def generate_content(data: PromptRequest):
    await asyncio.sleep(1.5)
    concept = data.concept
    level=data.level

    # Simple rule-based responses
    # if "machine learning" in user_prompt:
    #     return {
    #         "result": "Machine Learning is a field of AI where systems learn patterns from data and make predictions without being explicitly programmed."
    #     }
    # elif "os" in user_prompt or "operating system" in user_prompt:
    #     return {
    #         "result": "An Operating System is system software that manages hardware, memory, processes and provides an interface between user and computer."
    #     }
    # elif "database" in user_prompt:
    #     return {
    #         "result": "A database is an organized collection of structured information stored electronically."
    #     }

    # else:
    #     return {
    #         "result": f"This is a simulated AI response for: {data.prompt}"
    #     }
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are an AI tutor that explains concepts and creates quizzes."
            # },
            {
                "role": "user",
                "content": f"""
            Explain the concept '{concept}' for {level} level.

            Then create 3 MCQ quiz questions.

            Return ONLY valid JSON in this format:

            {{
            "explanation": "short explanation here",
            "quiz": [
            {{
                "question": "question text",
                "options": ["A","B","C","D"],
                "answer": 0
            }}
            ]
            }}

            Do not include any extra text outside JSON.
            """
            }
        ]
    )

    ai_text = response.choices[0].message.content.strip()

    if ai_text.startswith("```"):
        ai_text = ai_text.split("```")[1]
    # print("AI RESPONSE:", ai_text)
    try:
        data = json.loads(ai_text)
        explanation = data["explanation"]
        quiz = data["quiz"]
    except:
        explanation = ai_text
        quiz = []
    

    return {
        "explanation": explanation,
        "quiz": quiz
    }