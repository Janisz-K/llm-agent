import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
)

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
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=SYSTEM_PROMPT),)
    
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count

    if response.text:
        print(response.text)
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    if cmd_verbose:
        print(f"User prompt: {args[0]}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")

if __name__ == "__main__":
    main()
