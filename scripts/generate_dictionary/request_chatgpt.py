import os
import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from models import WordEntry


SCRIPT_DIR = Path(__file__).parent
load_dotenv(SCRIPT_DIR / ".env")
PROMPT_FILE = SCRIPT_DIR / "prompt.txt"
DATA_DIR = SCRIPT_DIR / "data"


def load_prompt_template() -> str:
    """Load the prompt template from file."""
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    base_prompt = content.rsplit("Now, explain the German word:", 1)[0]
    return base_prompt + "Now, explain the German word: {word}"


def get_output_path(word: str) -> Path:
    """Get the output path for a word's JSON file."""
    first_letter = word[0].upper()
    return DATA_DIR / first_letter / f"{word}.json"


def load_words(filepath: str) -> list[str]:
    """Load words from a text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def is_corrupted(result: WordEntry) -> bool:
    """Check if the output contains JSON artifacts."""
    json_artifacts = ['},{', '{"', '"}', '[{', '}]']

    def check_text(text: str) -> bool:
        return any(artifact in text for artifact in json_artifacts)

    for meaning in result.meanings:
        if check_text(meaning.en) or check_text(meaning.cn):
            return True
        for example in meaning.examples:
            if check_text(example.de) or check_text(example.en) or check_text(example.cn):
                return True

    for collocation in result.collocations:
        if check_text(collocation.de) or check_text(collocation.en) or check_text(collocation.cn):
            return True

    if result.related_words:
        for word in result.related_words:
            if check_text(word.de) or check_text(word.en) or check_text(word.cn):
                return True

    return False


def request_chatgpt(word: str, prompt_template: str, llm, max_retries: int = 3) -> WordEntry:
    """Send request to ChatGPT and get structured output with retry logic."""
    prompt = prompt_template.format(word=word)

    for attempt in range(max_retries):
        print(f"  Attempt {attempt + 1}/{max_retries}...")
        result = llm.invoke(prompt)
        if not is_corrupted(result):
            return result
        print(f"  Corrupted output, retrying...")

    raise ValueError(f"Failed after {max_retries} retries due to corrupted output")


def save_result(word: str, result: WordEntry):
    """Save the result to a JSON file."""
    output_path = get_output_path(word)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, ensure_ascii=False, indent=2)
    print(f"Saved: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate German dictionary entries using ChatGPT")
    parser.add_argument("words_file", help="Path to text file containing German words (one per line)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    words = load_words(args.words_file)
    print(f"Loaded {len(words)} words")

    prompt_template = load_prompt_template()
    # model="gpt-5", model="gpt-4o"
    llm = ChatOpenAI(model="gpt-5", temperature=0, timeout=180).with_structured_output(WordEntry)

    for word in words:
        output_path = get_output_path(word)
        if output_path.exists() and not args.force:
            print(f"Skipping {word} (already exists)")
            continue

        print(f"Processing: {word}")
        try:
            result = request_chatgpt(word, prompt_template, llm)
            save_result(word, result)
        except Exception as e:
            print(f"Error processing {word}: {e}")
            # Save empty JSON for failed words
            output_path = get_output_path(word)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({"error": str(e)}, f, ensure_ascii=False, indent=2)
            print(f"Saved empty: {output_path}")

    print("Done!")


if __name__ == "__main__":
    main()
