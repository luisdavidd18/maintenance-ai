import requests

print("\n🔧 AI Maintenance Copilot")
print("-------------------------")

failure = input(
    "\nDescribe the equipment failure:\n> "
)

prompt = f"""
You are an industrial reliability engineering assistant.

Analyze the following equipment failure:

{failure}

Your job is to assist a maintenance engineer, not replace one.

Return:

1. PROBABLE CAUSES
Rank the most plausible causes from highest to lowest probability.
Explain why each cause fits the available evidence.

2. IMMEDIATE TROUBLESHOOTING
Give specific checks a maintenance technician should perform.

3. SAFETY
Identify relevant electrical, mechanical, thermal, pressure,
stored-energy, or lockout/tagout concerns.

4. DATA TO COLLECT
Identify measurements or observations that would help distinguish
between possible causes.

5. ROOT CAUSE QUESTIONS
Provide questions that should be answered during an RCA investigation.

Clearly distinguish facts from hypotheses.
Do not invent measurements.
Do not claim certainty when evidence is insufficient.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
    },
)

response.raise_for_status()

data = response.json()

print("\n🤖 ANALYSIS\n")
print(data["response"])