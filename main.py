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
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
)

def call_function (function_call_part, verbose = False):
    function_name = function_call_part.name
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

    function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": result},
        )
    ],
)



def main():

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    cmd_verbose = False

    for arg in args:
        if arg == "--verbose":
            cmd_verbose = True

    loop_times = 0
    messages = [ types.Content(role="user", parts = [types.Part(text=args[0])])]

    while loop_times < 21:
        loop_times += 1
        response = client.models.generate_content(
                model="gemini-2.0-flash-001",    
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions],system_instruction=SYSTEM_PROMPT),)
        
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        prompt_token = response.usage_metadata.prompt_token_count
        response_token = response.usage_metadata.candidates_token_count
        

        
        function_responses = []
        if response.function_calls:
            for function_call_part in response.function_calls:
                func_return = call_function(function_call_part, cmd_verbose)
                if not func_return.parts[0]:
                    raise Exception ("Fatal Error")
                if cmd_verbose:
                    print(f"-> {func_return.parts[0].function_response.response}")
                function_responses.append(func_return.parts[0])
            messages.append(types.Content(role = "user", parts = function_responses))

            if not function_responses:
                raise Exception("no function responses generated, exiting.")
            continue
        
        elif response.text:
            print("Final response:")
            print(response.text)
            break
        else:
            raise Exception("Response has neither function calls nor text")


    if cmd_verbose:
        print(f"User prompt: {args[0]}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")

if __name__ == "__main__":
    main()
