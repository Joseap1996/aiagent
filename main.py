import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()
    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = args[0]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages =[
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if "--verbose" in args:
        generate_content_verbose(client,messages,user_prompt)
    else:
        generate_content(client,messages)

def generate_content_verbose(client,messages, user_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("Response:")
    print(response.text)
    print("User prompt: ",user_prompt)
    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)


def generate_content(client,messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
