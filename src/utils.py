import openai
from src.config import Config
import requests
import base64
from datetime import datetime
import json


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def process_receipt(image_path):
    date = datetime.today().strftime("%Y-%m-%d")
    prompt = (
        f"""Return the items on the receipt in json format, 
    only including the name, quantity, and an esimated expiry date. 
    The current date is {date}.
    
    An example json response would look like the following:\n\n"""
        + """{"items": [{"name": "Milk", "quantity": 1, "estimated_expiry_date": "2024-06-02"}]}"""
    )
    openai.api_key = Config.OPENAI_API_KEY
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }
    payload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    print("OPENAI RESPONSE: ", response.json()["choices"][0]["message"]["content"])
    return json.loads(response.json()["choices"][0]["message"]["content"])["items"]
