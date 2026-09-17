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
  "hypotheses": [
    {{
      "cause": "string",
      "why_it_fits": "string",
      "evidence_to_confirm": ["string"],
      "evidence_against": ["string"]
    }}
  ],
  "next_best_checks": ["string"],
  "safety_considerations": ["string"],
  "data_to_collect": ["string"],
  "rca_questions": ["string"]
}}

Diagnostic requirements:
- Generate at least 5 distinct hypotheses when plausible.
- Do not repeat the symptom as a cause.
- Avoid vague labels such as "process variability" unless you identify the specific mechanism.
- Prefer specific physical or process mechanisms over broad categories.
- Do not anchor on a single cause unless the evidence strongly supports it.
- For every hypothesis, explain why it fits.
- For every hypothesis, provide evidence that would support it.
- For every hypothesis, provide evidence that would weaken or eliminate it.
- Include relevant mechanical, electrical, control, process, material, and operating-condition hypotheses when applicable.
- Do not invent machine design details that were not provided.
- Do not invent measurements or observations.

Next-check requirements:
- Recommend checks that distinguish between competing hypotheses.
- Prioritize checks that are fast, safe, and highly diagnostic.
- Avoid generic instructions such as "inspect the machine."

RCA question requirements:
- Ask diagnostic questions that help confirm or eliminate hypotheses.
- Ask about repeatability, timing, machine speed, load, temperature,
  vibration, noise, recent maintenance, station-specific behavior,
  operating changes, and whether the symptom follows a component or station.
- Avoid vague questions such as "What happened?"
- Avoid questions that simply restate the failure.

Safety requirements:
- Always evaluate lockout/tagout requirements.
- Consider rotating equipment, pinch points, stored mechanical energy,
  electrical hazards, hot surfaces, guarding, and unexpected motion.
- If information is insufficient, state what safety conditions must be verified.

Formatting requirements:
- Return ONLY JSON.
- Every field except "hypotheses" must be a JSON array of strings.
- "hypotheses" must be a JSON array of objects.
- Do not add markdown.
- Do not add commentary before or after the JSON.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:3b-instruct",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "num_predict": 900
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


print("\n🤖 DIAGNOSTIC ANALYSIS\n")

print("HYPOTHESES")

for index, item in enumerate(result.get("hypotheses", []), start=1):
    if not isinstance(item, dict):
        continue

    print(f"\n{index}. {item.get('cause', 'Unknown cause')}")

    print("   Why it fits:")
    print(f"   - {item.get('why_it_fits', 'No explanation provided')}")

    print("   Evidence to confirm:")
    for evidence in normalize_list(item.get("evidence_to_confirm", [])):
        print(f"   - {evidence}")

    print("   Evidence against:")
    for evidence in normalize_list(item.get("evidence_against", [])):
        print(f"   - {evidence}")


print("\nNEXT BEST CHECKS")
for item in normalize_list(result.get("next_best_checks", [])):
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