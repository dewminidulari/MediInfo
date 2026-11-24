from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from your computer

SYSTEM = """You explain medicine information in simple language.
Use ONLY the label data provided. Never add facts from your own knowledge.
If something is missing from the data, say 'not available in the source'.
Do not give dose advice or tell the user whether they should take the medicine.
End with: 'This is general information. Ask a doctor or pharmacist before use.'"""

def explain(info: dict) -> str:
    prompt = (
        f"Label data:\n{info}\n\n"
        "Explain: what it is used for, key warnings, "
        "common side effects, and interactions."
    )
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM),
    )
    return response.text