import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) > 1:
        content = sys.argv[1]
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=content
        )
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("error, no prompt given")
        sys.exit(1)
if __name__ == "__main__":
    main()
