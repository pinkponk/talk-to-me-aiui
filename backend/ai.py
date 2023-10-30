import base64
import json
import logging
import os
import time

import openai

AI_COMPLETION_MODEL = os.getenv("AI_COMPLETION_MODEL", "gpt-3.5-turbo")
LANGUAGE = os.getenv("LANGUAGE", "en")

# Read the prompt.txt file into the INITIAL_PROMPT variable
with open("prompt.txt", "r") as f:
    INITIAL_PROMPT = f.read()

async def get_completion(user_prompt, conversation_thus_far):
    if _is_empty(user_prompt):
        raise ValueError("empty user prompt received")

    start_time = time.time()
    messages = [
        {
            "role": "system",
            "content": INITIAL_PROMPT
        }
    ]

    messages.extend(json.loads(base64.b64decode(conversation_thus_far)))
    messages.append({"role": "user", "content": user_prompt})

    logging.debug("calling %s", AI_COMPLETION_MODEL)
    res = await openai.ChatCompletion.acreate(model=AI_COMPLETION_MODEL, messages=messages, timeout=15)
    logging.info("response received from %s %s %s %s", AI_COMPLETION_MODEL, "in", time.time() - start_time, "seconds")

    completion = res['choices'][0]['message']['content']
    logging.info('%s %s %s', AI_COMPLETION_MODEL, "response:", completion)

    return completion


def _is_empty(user_prompt: str):
    return not user_prompt or user_prompt.isspace()
