import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():

    args = sys.argv[1:]

    if not args:
        raise Exception ("No prompt provided")
    
    cmd_verbose = False

    for arg in args:
        if arg == "--verbose":
            cmd_verbose = True


    messages = [ types.Content(role="user", parts = [types.Part(text=args[0])])]
    response = client.models.generate_content(
            model="gemini-2.0-flash-001",    
            contents=messages)
    
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count

    print(response.text)
    
    if cmd_verbose:
        print(f"User prompt: {args[0]}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")

if __name__ == "__main__":
    main()
