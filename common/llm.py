import os, time
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.environ["GEMINI_API_KEY"],
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
SMALL, BIG = "gemini-3.5-flash-lite", "gemini-3.8-flash"


def chat(model, messages, **kw):
    return client.chat.completions.create(model=model, messages=messages,
                                          **kw)