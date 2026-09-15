import json
import requests

print("\n🔧 AI Maintenance Copilot")
print("-------------------------")

failure = input("\nDescribe the equipment failure:\n> ")

prompt = f"""
You are an industrial reliability engineering assistant.

Analyze this equipment failure:

{failure}

Return ONLY valid JSON using exactly this structure:

{{
  "probable_causes": [
    {{
      "cause": "string",
      "reason": "string"
    }}
  ],
  "immediate_checks": ["string"],
  "safety_considerations": ["string"],
  "data_to_collect": ["string"],
  "rca_questions": ["string"]
}}

Rules:
- Do not add markdown.
- Do not add commentary before or after the JSON.
- Do not invent measurements.
- Clearly separate evidence from hypotheses.
- Keep the response concise and technically useful.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "num_predict": 500
        }
    },
)

response.raise_for_status()

raw_output = response.json()["response"]

try:
    result = json.loads(raw_output)
except json.JSONDecodeError:
    print("\nThe model returned invalid JSON.")
    print("\nRaw response:\n")
    print(raw_output)
    raise

print("\n🤖 STRUCTURED ANALYSIS\n")

print("PROBABLE CAUSES")
for item in result["probable_causes"]:
    print(f"- {item['cause']}: {item['reason']}")

print("\nIMMEDIATE CHECKS")
for item in result["immediate_checks"]:
    print(f"- {item}")

print("\nSAFETY CONSIDERATIONS")
for item in result["safety_considerations"]:
    print(f"- {item}")

print("\nDATA TO COLLECT")
for item in result["data_to_collect"]:
    print(f"- {item}")

print("\nRCA QUESTIONS")
for item in result["rca_questions"]:
    print(f"- {item}")