import time
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_chat(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            import traceback
            print("FULL ERROR:")
            traceback.print_exc()

            if attempt < 2:
                time.sleep(5)
            else:
                return "Gemini service temporarily unavailable. Please try again later."