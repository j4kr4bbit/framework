from fastapi import FastAPI
import os
import pandas as pd
from sqlalchemy import create_engine
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
from sqlalchemy.sql import text
from transformers import TextStreamer
from transformers import pipeline, AutoTokenizer
from datetime import datetime

#Database Information
db = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@postgres/{db}')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/PostgreSQL_test")
async def testing():
    user = {"Task" : ["Task 1"],
            "Start" : ["2023-12-15 01:00:00"],
            "Finish" : ["2023-12-15 01:54:08"]}
    df = pd.DataFrame(user)
    df.to_sql('PG_test', con=engine, if_exists='append')
    return df.to_dict(orient="records")


class DB_Info(BaseModel):
    chatid: str
    userid: Optional[str]

class Prompt(BaseModel):
    question: str
    chatid: str
    userid: str

class chatid(BaseModel):
    chatid: str

@app.get("/add/User/{Username}")
async def addUser(Username):
    user = {'Username' : [f"{Username}"],
            'user_id' : [str(uuid.uuid4())],
            'chat_id' : [str(uuid.uuid4())],
            'timestamp' : [datetime.now()]}
    df = pd.DataFrame(user)
    df.to_sql('testing_db', con=engine, if_exists='append')
    return df.to_dict(orient="records")

@app.post("/Data_Request")
async def data_req(c: chatid):
    df = pd.read_sql_query(f'SELECT * FROM "testing_db" WHERE "chat_id" = \'{c.chatid}\' ;', engine)
    return df.to_dict(orient="records")

@app.get("/All_ChatIDs")
async def database_test():
    df = pd.read_sql_query(f'SELECT DISTINCT "chat_id" FROM "Messages" ;', engine)
    return df.to_dict(orient="records")

app.delete("/reset_db")
async def reset_db(c: chatid):
    sql = f'''
    DELETE FROM "testing_db" WHERE "chat_id" IN (\'{c.chatid}\') RETURNING * ;'
    '''

    with engine.connect() as conn:
        query = conn.execute(text(sql))
        conn.commit()
    return {"success": "0"}


app.post("/query")
async def query(p: Prompt):
    question = p.question
    tokenizer = AutoTokenizer.from_pretrained("whatever_model")
    streamer = TextStreamer(tokenizer, skip_prompt=True)
    pipe = pipeline('text-generation', model='whatever_model', device_map='auto', streamer=streamer)
    """
    make catch for llm response
    """
    llm_response = "blah"
    init_message= {'user_id': [p.userid],
                   'chat_id' : [p.chatid],
                   'message' : [f"{question}"],
                   'message_type' : ["Human"],
                   'timestamp' : [f"{datetime.now()}"]}
    init_df = pd.DataFrame(init_message)
    init_df.to_sql("whatever", con=engine, if_exists="append")

    llm_message = {'user_id' : [p.userid],
                   "chat_id" : [p.chatid],
                   "message" : [f"{llm_response}"],
                   "message_type" : ["LLM"],
                    "timestamp" : [f"{datetime.now()}"]}

    return {"success" : "0"}












