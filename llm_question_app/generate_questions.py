import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

#API key added in .env file
#API used of gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it in a .env file or as an environment variable.")


genai.configure(api_key=API_KEY)

PROMPT_TEMPLATE = """
You are to generate 2 new math questions based on the style of the provided base questions.

Base Questions:
{base}

Curriculum Topics:
{curr}

Output MUST follow exactly this format:

@title <meaningful title>
@description <brief description>

// For each question:
@question <The question here. Include LaTeX if needed and an embedded image placeholder like ![image](image1.png)>
@instruction <instructions for answering>
@difficulty <easy, moderate, hard>
@Order <question number>
@option <option 1>
@option <option 2>
@@option <correct option>
@option <option 4>
@explanation <explanation text>
@subject <subject from provided curriculum>
@unit <unit from provided curriculum>
@topic <topic from provided curriculum>
@plusmarks 1

IMPORTANT:
- Replace ![image](image1.png) with an IMAGE PROMPT in curly braces like {{IMAGE PROMPT: detailed description of the image}}.
- The image prompt must describe the diagram in enough detail so it can be generated later with Bing Image Creator or Stable Diffusion.
- Make sure both questions are DIFFERENT in topic but match the style of the base questions.
"""


def read_file(file_path):
    """Reads and returns the content of a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(base_text, curriculum_text):
    """Builds the final LLM prompt."""
    return PROMPT_TEMPLATE.format(base=base_text, curr=curriculum_text)

def generate_questions(prompt):
    """Generates new questions using Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def main(args):
    # Read input files
    base_questions = read_file(args.base_file)
    curriculum = read_file(args.curriculum_file)

    # Build prompt
    prompt = build_prompt(base_questions, curriculum)

    # Generate questions
    print("🚀 Generating questions...\n")
    result = generate_questions(prompt)

    # Print final output
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate math questions from base questions using Gemini API.")
    parser.add_argument("--base_file", type=str, default="C:/Users/dsuya/Desktop/llm_question_app/base_questions.txt", help="Path to text file containing base questions")
    parser.add_argument("--curriculum_file", type=str, default="curriculum.txt", help="Path to text file containing curriculum list")
    args = parser.parse_args()
    main(args)

