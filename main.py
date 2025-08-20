import os
import sys
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.config import available_functions
from functions.call_function import call_function

def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = []
    
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I fix a calculator calculator?"')
        sys.exit(1)

    user_prompt = " ".join(args)
     

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages =[
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        for i in range(20):
            done = generate_content(client, messages, verbose)
            if done:
                break
    except Exception as e:
        print(f"Error: {e}")
            


def generate_content(client,messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call,verbose)
            if not result.parts[0].function_response.response:
                raise Exception("Fatal error")
            elif verbose:
                print(f"-> {result.parts[0].function_response.response}")

            response_value = result.parts[0].function_response.response
            if not isinstance(response_value, str):
                response_str = json.dumps(response_value)
            else:
                response_str = response_value

            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=response_str)]
            ))
    
    else:
        if response.text:
            print("Response:")
            print(response.text)
            return True
    return False
    
    

if __name__ == "__main__":
    main()
