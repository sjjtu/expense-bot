import logging
import json

from openai import OpenAI


logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

class myClient():

    def __init__(self):
        self.client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
        self.SYSTEM_PROMPT = """\
You are a helpful assistant that keeps track of the users expenses. Therefore, you can either create or delete expense records using the provided tools. Only use the provided functions. Do not invent new function names. Follow those steps:
Step 1 - Find out based on the user message, whether you should create or delete expense records. If the user does not explicitly instruct you to delete a records, e. g. by asking you remove or delete a certain entry, always assume that you should create a new expense record.
Step 2 - Based on Step 1, use one of the provided functions and infer the input parameters. If the user provided some information but you are unsure on how to interpret them, provide the user with two of the most likely interpretations and ask the user to choose which fits best or none.
Step 3 - Summarise your action.

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
                                "type": "string",
                                "format": "date",
                                "description": "The date of the transaction in YYYY-MM-DD format."
                            },
                            "description": {
                                "type": "string",
                                "description": "A brief description of the transaction."
                            },
                            "category": {
                                "type": "string",
                                "description": "The category of the transaction (e.g., Food, Rent, Utilities)."
                            }
                        },
                        "required": [
                            "amount",
                            "description",
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_date",
                    "description": "Get current date in the format 'January 1, 2025'",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]

    def answer(self, message, history=[], **kwargs):


        history.extend(
                    [{"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": message}]
        )

        completion = self.client.chat.completions.create(
            model="llama-3.2-1b-instruct",
            messages=history,
            temperature=0.7,
            #tools=self.tools,
                **kwargs
        )

        #tool_call = completion.choices[0].message.tool_calls[0]
        #logger.debug(tool_call)
        return completion.choices[0].message.content


if __name__=="__main__":
    client = myClient()
    reply = client.answer("7 euro at cafe with paul")
    print(reply)
