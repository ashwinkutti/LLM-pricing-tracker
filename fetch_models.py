import json
import os

from openai import OpenAI

# ------------------------------------------------
# OPENAI CLIENT
# ------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


models_response = client.models.list()

models_data = []

for model in models_response.data:

    models_data.append({
        "provider": "OpenAI",
        "model": model.id,
        "parameters": "Unknown",
        "context_window": "Unknown",
        "input_price": "Unknown",
        "output_price": "Unknown",
        "best_for": "General AI tasks",
        "speed": "Unknown"
    })
# Save dynamic JSON
with open("dynamic_models.json", "w") as f:
    json.dump(models_data, f, indent=2)

print("✅ dynamic_models.json generated successfully")
