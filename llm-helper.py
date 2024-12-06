import os
from openai import OpenAI

if "OPENAI_API_KEY" not in os.environ:
    exit(1)


client = OpenAI()
SYSTEM_PROMPT = """You are a helpful coding assistant that suggests a one-line bash command based on the user's query."""
FEW_SHOT_PROMPTS = [
    ('''How do I remove the file called "hello" from my home directory?''', '''cd ~ && rm "hello"'''),
    ('''I want to print "donkey" in my terminal''', '''echo "donkey"'''),
    ('''Rename the file "papa.txt" to "mama.txt"''', '''mv "papa.txt" "mama.txt"''')
]


def create_messages(prompt):
    few_shot_prompts = []
    for query, answer in FEW_SHOT_PROMPTS:
        few_shot_prompts.append({"role": "user", "content": query})
        few_shot_prompts.append({"role": "assistant", "content": answer})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + few_shot_prompts + [{"role": "user", "content": prompt}]

    return messages


def suggest_command(prompt):
    messages = create_messages(prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content


def run_command(command):
    print(command)
    user_input = input("Run the above command (y/n): ")
    if user_input.lower() == "y":
        output = os.popen(command).read()
        print("Command output:")
        print(output)


if __name__ == "__main__":
    print("Welcome to this LLM command-line helper. This utility suggests bash commands based on the user's prompt.")
    user_input = input("Enter the prompt: ")
    command = suggest_command(user_input)
    run_command(command)
