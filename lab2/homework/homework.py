from transformers import pipeline
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI()

with open("api_key.txt", 'r') as file:
    API_KEY = file.read().strip()

@app.get("/")
async def root():
    if not os.path.exists('form.html'):
        return HTMLResponse("<h1>No Form file!</h1>", 501)
    return FileResponse("form.html", 200)

@app.get("/horoscope")
async def horoscope(sign: str, time: str, question: str):
    url1 = f"https://horoscopes-ai.p.rapidapi.com/get_horoscope_en/{sign}/{time}/general"
    headers1 = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "horoscopes-ai.p.rapidapi.com"
    }
    response1 = requests.get(url1, headers=headers1)
    r1 = response1.json()

    if not r1:
        return HTMLResponse("<h1>Couldnt process the request</h1>", 400)
    if not response1.ok:
        return HTMLResponse("<h1>Couldnt get the first horoscope</h1>", response1.status_code)

    url2 = "https://daily-horoscope-api.p.rapidapi.com/api/Daily-Horoscope-English/"
    querystring = {"zodiacSign" : sign, "timePeriod" : time}
    headers2 = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "daily-horoscope-api.p.rapidapi.com"
    }
    response2 = requests.get(url2, headers=headers2, params=querystring)
    r2 = response2.json()

    if not r2:
        return HTMLResponse("<h1>Couldnt process the request</h1>", 400)
    if not response2.ok:
        return HTMLResponse("<h1>Couldnt get the second horoscope</h1>", response2.status_code)

    context1 = ''.join(r1["general"])
    context2 = ''.join(r2["prediction"])
    context = context1 + context2

    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    QA = {'question': question, 'context': context}
    res = nlp(QA)
    answer = res["answer"]

    return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Horoscope</title>
        </head>
        <body>
            <h1>Answer to your question {question} is:</h1>
            <h3>{answer}</h3>
        </body>
        </html>
    """)
