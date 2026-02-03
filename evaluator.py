import os
import json
from dotenv import load_dotenv
from langfuse.openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_resume(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume screening assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )

        output = response.choices[0].message.content

        # Extract JSON safely
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_text = output[json_start:json_end]

        return json.loads(json_text)

    except Exception as e:
        print("Error during resume evaluation:", e)
        return None