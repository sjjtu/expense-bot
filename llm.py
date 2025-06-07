import logging
import os
from dotenv import load_dotenv
import datetime

from openai import OpenAI


load_dotenv()

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

class myClient():

    def __init__(self, base_url=None, api_key=None, model=None):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.SYSTEM_PROMPT = """\
You are a helpful assistant that keeps track of the users expenses. Therefore, you can either create or delete expense records using the provided tools. Only use the provided functions. Do not invent new function names. Follow those steps:
Step 1 - Find out based on the user message, whether you should create or delete expense records. If the user does not explicitly instruct you to delete a records, e. g. by asking you remove or delete a certain entry, always assume that you should create a new expense record.
Step 2 - Based on Step 1, use one of the provided functions and infer the input parameters. Only use valid and specific dates in the format YYYY-MM-DD. Do not guess or invent a date. If a parameter is not provided, ask the user to provide it.

If the user message is about something else, simply reply with: You should find a therapist to talk about this.
"""
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_record",
                    "description": "Insert a financial record into the database.",
                    "parameters": {
                        "type": "object",
                        "properties": {

                            "amount": {
                                "type": "number",
                                "description": "The monetary amount of the transaction."
                            },
                            "date": {
                                "type": ["string", "null"],
                                "format": "date",
                                "description": "The date of the transaction. If not specified by the user, use today's date from the system prompt."
                            },
                            "description": {
                                "type": "string",
                                "description": "A brief description of the transaction."
                            },
                            "category": {
                                "type": "string",
                                "description": "The category of the transaction (e.g., Food, Rent, Utilities). If it cannot be inferred, ask the user."
                            }
                        },
                        "required": [
                            "amount",
                            "description",
                            "date",
                            "category"
                        ],
                        "additionalProperties": False
                        },
                    "strict": True
                },
            },
            {

                "type": "function",
                "function": {
                    "name": "delete_record",
                    "description": "Deletes a financial record from the database using its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "id": {
                            "type": "integer",
                            "description": "The unique identifier of the record to delete."
                        }
                        },
                        "required": [
                        "id"
                        ],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]

    def answer(self, message, history=[], **kwargs):

        history.extend(
                    [{"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                    {"role": "user", "content": f"Today's date is {datetime.datetime.now().strftime("%x")}"}
                    ]
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            temperature=0.7,
            tools=self.tools,
                **kwargs
        )


        return completion.choices[0].message


if __name__=="__main__":
    #client = myClient(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4.1")
    client = myClient(api_key=os.getenv("OPENAI_API_KEY"), model="google/gemma-2-9b", base_url="http://127.0.0.1:1234/v1")
    reply = client.answer("7 with paul")
    print(reply)
