import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def evaluate_resume(prompt: str):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 800
            }
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        print("Ollama response status:", response.status_code)
        if response.status_code != 200:
            print("Ollama error:", response.text)
            return None

        output = response.json()["response"]

        # Extract JSON safely from model output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            print("Invalid JSON returned by Llama model")
            print(output)
            return None

        json_text = output[json_start:json_end]

        return json.loads(json_text)

    except Exception as e:
        print("Error during Llama 3.2 resume evaluation:", e)
        return None