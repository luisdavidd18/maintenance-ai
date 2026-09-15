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
- Return ONLY valid JSON.
- Every field except "probable_causes" must be a JSON array of strings.
- Never return a plain string where an array is expected.
- Do not add markdown.
- Do not add commentary before or after the JSON.
- Do not invent measurements.
- Clearly separate evidence from hypotheses.
- Keep the response concise and technically useful.

Safety requirements:
- Always evaluate lockout/tagout requirements.
- Consider rotating equipment, pinch points, stored mechanical energy,
  electrical hazards, hot surfaces, guarding, and unexpected motion.
- Never say "no special safety considerations" for industrial machinery.
- If information is insufficient, state what safety conditions must be verified.

Diagnostic reasoning requirements:
- Generate multiple plausible failure modes from the symptoms provided.
- Do not anchor on one cause unless the evidence clearly supports it.
- For each probable cause, explain:
  1. Why it fits the symptom
  2. What evidence would confirm it
  3. What evidence would make it less likely
- Include mechanical, electrical, process, material, and operating-condition causes when relevant.
- Do not assume components are functioning correctly just because the machine is operating.
- Do not invent machine design details that were not provided.

RCA question requirements:
- Ask questions that help eliminate or confirm competing hypotheses.
- Focus on differences between stations, machine speed, load, timing, temperature,
  vibration, noise, recent maintenance, repeatability, and operating conditions.
- Avoid vague questions such as "What happened?" or "What is the root cause?"
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

def normalize_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value]
    return []

print("\n🤖 STRUCTURED ANALYSIS\n")

print("PROBABLE CAUSES")
for item in result.get("probable_causes", []):
    if isinstance(item, dict):
        print(f"- {item.get('cause', 'Unknown')}: {item.get('reason', '')}")
    else:
        print(f"- {item}")

print("\nIMMEDIATE CHECKS")
for item in normalize_list(result.get("immediate_checks", [])):
    print(f"- {item}")

print("\nSAFETY CONSIDERATIONS")
for item in normalize_list(result.get("safety_considerations", [])):
    print(f"- {item}")

print("\nDATA TO COLLECT")
for item in normalize_list(result.get("data_to_collect", [])):
    print(f"- {item}")

print("\nRCA QUESTIONS")
for item in normalize_list(result.get("rca_questions", [])):
    print(f"- {item}")