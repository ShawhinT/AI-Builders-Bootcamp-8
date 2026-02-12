# Generate LinkedIn posts from user inputs

from openai import OpenAI
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# define prompt path
prompt_path = "prompts/prompt-v3"

# connect to openai API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# funtion to generate posts
def generate_post(instructions, user_input):
    response = client.responses.parse(
        model="gpt-5",
        instructions=instructions,
        input=user_input,
    )
    return response.output_text


# load instructions
with open(f"{prompt_path}.md", "r") as file:
    instructions = file.read()

# read inputs from inputs.csv and store in a list
with open("data/_inputs/30-post-ideas.csv", "r") as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    user_input_list = [row[0] for row in reader]  # Extract first element from each row

# generate posts for each input
output_data = []
for i, user_input in enumerate(user_input_list, 1):
    llm_output = generate_post(instructions, user_input)
    output_data.append([user_input, llm_output])
    print(f"Generated post {i} of {len(user_input_list)}")

# save results to CSV
today = datetime.now().strftime("%Y-%m-%d")
prompt_version = prompt_path.split("-")[-1]  # Extract 'v3' from 'prompts/prompt-v3'
# Create date-based directory if it doesn't exist
date_dir = f"data/{today}_prompt-{prompt_version}"
os.makedirs(date_dir, exist_ok=True)

filename = f"{date_dir}/request_response.csv"
with open(filename, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["User Input", "LLM Output"])  # header row
    writer.writerows(output_data)

print(f"Successfully generated {len(output_data)} posts and saved to {filename}")

