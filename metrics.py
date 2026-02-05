import tiktoken
import time

MODEL_COST = {
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,    # $ per token
        "output": 0.0006 / 1000
    }
}

def count_tokens(text, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def calculate_cost(prompt_tokens, completion_tokens, model="gpt-4o-mini"):
    pricing = MODEL_COST[model]

    cost = (
        prompt_tokens * pricing["input"] +
        completion_tokens * pricing["output"]
    )

    return cost


class MetricSnapshot:
    def __init__(self):
        self.start = time.time()
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cost = 0
        self.latency = 0

    def stop(self):
        self.latency = round(time.time() - self.start, 2)