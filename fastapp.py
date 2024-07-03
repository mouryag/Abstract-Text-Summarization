from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Importing the provided code from summarizer.py
from summarize import text_summarize

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class SummarizeRequest(BaseModel):
    text: str
    content_type: str


@app.get("/", response_class=HTMLResponse)
async def read_form():
    with open("static/summarization.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content

@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    try:
        # Capture the summarization output
        summary = []
        for content in text_summarize(request.text, request.content_type):
            summary.append(content)
        summary_text = ''.join(summary)
        return {"summary": summary_text}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except TypeError as te:
        raise HTTPException(status_code=400, detail=str(te))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# To run the app, use: uvicorn main:app --reload
