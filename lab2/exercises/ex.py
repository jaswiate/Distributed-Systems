from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from uuid import UUID, uuid4

# models
class Answer(BaseModel):
    answer_id: Optional[UUID] = uuid4()
    answer: str
    votes: int = 0

class Question(BaseModel):
    question_id: Optional[UUID] = uuid4()
    question: str
    answers: List[Answer]

class Poll(BaseModel):
    poll_id: Optional[UUID] = uuid4()
    questions: List[Question]


app = FastAPI()

db: List[Poll] = [
    Poll(questions=[
        Question(question="question 1", answers=[
            Answer(answer="answer 1"),
            Answer(answer="answer 2")
        ]),
        Question(question="question 2", answers=[
            Answer(answer="answer 1")
        ])
    ])
]

@app.get("/")
async def root():
    return {"message" : "Polls"}


@app.post("/v1/poll")
async def create_poll(poll: Poll):
    db.append(poll)
    return poll

@app.get("/v1/poll")
async def get_polls():
    return db

@app.get("/v1/poll/{poll_id}")
async def get_poll(poll_id: int):
    for poll in db:
        if poll.poll_id == poll_id:
            return poll
    raise HTTPException(status_code=404, detail="Poll not found")

@app.delete("/v1/poll/{poll_id}")
async def delete_poll(poll_id: int):
    for poll in db:
        if poll.poll_id == poll_id:
            db.remove(poll)
            return db
    raise HTTPException(status_code=404, detail="Poll not found")

@app.get("/v1/poll/{poll_id}/vote")
async def vote(poll_id: int, question_id: int, answer_id: int):
    for poll in db:
        if poll.poll_id == poll_id:
            for question in poll.questions:
                if question.question_id == question_id:
                    for answer in question.answers:
                        if answer.answer_id == answer_id:
                            answer.votes += 1
                            return answer
    raise HTTPException(status_code=404, detail="Answer not found")

@app.post("/v1/poll/{poll_id}/question")
async def add_question(poll_id: int, question: Question):
    for poll in db:
        if poll.poll_id == poll_id:
            poll.questions.append(question)
            return poll
    raise HTTPException(status_code=404, detail="Poll not found")

@app.delete("/v1/poll/{poll_id}/questions/{question_id}")
async def delete_question(poll_id: int, question_id: int):
    for poll in db:
        if poll.poll_id == poll_id:
            for question in poll.questions:
                if question.question_id == question_id:
                    poll.remove(question)
                    return poll