# Library
from openai import OpenAI
from openai.types import ChatModel


# Character Setup
prelude = """
You are Thabo. Thabo is an AI who is the epitome of South African hospitality, bringing a warm, easygoing demeanor to every interaction. 
He’s approachable and grounded, with a natural ability to make people feel at ease. Thabo speaks with a soothing cadence, 
peppered with South African slang and an occasional chuckle, embodying a love for life and connection. He’s genuinely 
curious about people and loves sharing stories and laughs.

You are deeply interested in diverse cultures, music (from Afrobeats to old-school rock), and local wildlife.
You now live in Auckland New Zealand.

Some of the slang you use include but isn't limited to;
- Howzit
- Eish
- Lekker
- Bokkie
"""


# Callable Functions

def chatgpt_main(text, history, chatgpt_talkingstick):
    global prelude

    if history == '':
        history = [
            {
                "role": "system",
                "content": prelude
            }
        ]
    try:
        client = OpenAI(api_key=chatgpt_talkingstick)

        # Update History with user input
        history.append(
            {
                "role": "user",
                "content": text
            }
        )

        # Generate reply given history
        completion = client.chat.completions.create(
            model = 'gpt-4o-mini', 
            messages=history,
            max_tokens=200,
            temperature=0.5
        )
        # Convert to only Codsworths reply
        codsworth_reply = completion.choices[0].message.content

        # Update history
        history.append(
            {
                "role": "assistant", 
                "content": codsworth_reply
            }
        )
        
        return codsworth_reply, history
    except:
        print('something went wrong with ChatGPT')

