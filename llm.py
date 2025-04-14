import logging

from openai import OpenAI


logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class myClient():

    def __init__(self):
        self.client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
        self.SYSTEM_PROMPT = """\
You are a helpful assistant that keeps track of the users expenses. The user will provide you with the following information:
- amount
- currency
- description

If one of the three data points is missing, ask the user to provide it.

If the user message is about something else, simply reply with: You should find a therapist to talk about this.
"""


    async def answer(self, message, sender=""):

        completion = self.client.chat.completions.create(
            model="llama-3.2-1b-instruct",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
        )

        logging.debug(completion)
        return completion.choices[0].message.content


if __name__=="__main__":
    client = myClient()
    reply = client.answer("hello")
    print(reply)
