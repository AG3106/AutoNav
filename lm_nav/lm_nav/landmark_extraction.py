import os
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
import spacy
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()

# Prompts
PROMPT = """Take right next to an old white building. Look for a fire station, which you will see after passing by a school.
Ordered landmarks:
1. an old white building
2. a school
3. a fire station

Go straight for two blocks. Take right at a roundabout, before it you will pass a big, blue tree.
Ordered landmarks:
1. a big, blue tree
2. a roundabout

Look for a library, after taking a right turn next to a statue.
Ordered landmarks:
1. a statue
2. a library"""

SIMPLIFIED_PROMPT = """Look for a library, after taking a right turn next to a statue.
Landmarks:
1. a statue
2. a library

Look for a statue. Then look for a library. Then go towards a pink house.
Landmarks:
1. a statue
2. a library
3. a pink house"""


# Utility functions
def remove_article(string):
    articles = {"a", "an", "the"}
    return " ".join([w for w in string.split() if w.lower() not in articles])


def text_to_landmarks_spacy(text: str) -> List[str]:
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    blacklist = {"you", "left", "right", "left turn", "right turn"}
    return [chunk.text for chunk in doc.noun_chunks if remove_article(chunk.text.lower()) not in blacklist]


# Gemini API call
def generic_language_model_api_call_gemini(
    text: str, postprocess: bool = False, simple_prompt: bool = False
) -> List[str]:

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env file")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = SIMPLIFIED_PROMPT if simple_prompt else PROMPT
    prompt += "\n\n" + text + "\n"
    prompt += "Landmarks" if simple_prompt else "Ordered landmarks"
    prompt += ":\n1."

    response = model.generate_content(prompt)
    landmark_text = response.text.strip()
    landmarks = [s[s.find(". ") + 2:] for s in landmark_text.split("\n") if s.strip()]

    if postprocess:
        landmarks = [lm for lm in landmarks if lm]

    return landmarks


def text_to_landmarks_gemini(text: str, simple_prompt: bool = False) -> List[str]:
    return generic_language_model_api_call_gemini(text, postprocess=True, simple_prompt=simple_prompt)


# Example usage
if __name__ == "__main__":
    example_text = "Take a left after the post office and look for the red church next to the river."
    landmarks = text_to_landmarks_gemini(example_text, simple_prompt=True)
    print("Extracted Landmarks:", landmarks)
