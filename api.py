"""

get the API key:
https://aistudio.google.com/app/api-keys

how to API call:
https://ai.google.dev/gemini-api/docs/quickstart

API libraries installation (pip-25.3):
pip install -U google-genai python-dotenv
python.exe -m pip install --upgrade pip

GitHub Secrets:
1. Go to GitHub Website (for the repository running the Action)
2. "Settings" → "Secrets and variables" → "Actions"
3. "New repository secret"
4. Name: GEMINI_API_KEY
5. Paste API key

"""

import sys
import os
from google import genai
from dotenv import load_dotenv # API key (environment variable) is in env file

# read .env file and load variables into the system
load_dotenv()

# check if API key was found
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: API key not found.")
    sys.exit(1) # error code

# the client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=api_key)

# catch the file (file to be commented) name from the command line
# command format: python api.py <filename>

# TODO: for now, comments only first argument and ignores the rest
# check if there is an argument
if len(sys.argv) < 2:
    print("Usage: python api.py <filename>")
    sys.exit(1)

# catch file name
filename = sys.argv[1]

# try to open file and catch its content
try:
    with open(filename, "r", encoding="utf-8") as f:
        code_content = f.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)

# API call prompt
prompt = f"""
Read the python file and add one comment per function explaining the content of the function.
Do not alter the function; just add one comment line above it.
Return only the python raw code with comments.
Do not use markdown formatting such as ```python.

Code: 
{code_content}
"""

# API call
print("calling API")
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt
)

# write commented code to the file
with open (filename, "w", encoding="utf-8") as f:
    f.write(response.text)
print("OK")