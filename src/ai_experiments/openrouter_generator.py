import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import time

from openai import RateLimitError, APIError, APITimeoutError


def call_model(prompt: str, max_attempts: int = 3) -> str:
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}...")

        try:
            response = client.chat.completions.create(
                model="nvidia/nemotron-3-nano-30b-a3b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
            )

            if response.choices:
                content = response.choices[0].message.content

                if content:
                    print("Response received.")
                    return content

            error = getattr(response, "error", None)
            print("Empty response:", error)

        except RateLimitError as e:
            print(f"Rate limit error: {e}")

        except APITimeoutError as e:
            print(f"Timeout error: {e}")

        except APIError as e:
            print(f"API error: {e}")

        if attempt < max_attempts:
            wait_seconds = 15 * attempt
            print(f"Waiting {wait_seconds} seconds before retry...")
            time.sleep(wait_seconds)

    raise RuntimeError(
        f"Model failed after {max_attempts} attempts."
    )

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    timeout=120.0,
)


def generate_python_from_xml(class_xml: str, sequence_xml: str) -> str:
    prompt = f"""
You are given two UML diagrams exported from draw.io as XML.

1. The CLASS DIAGRAM defines:
- classes
- attributes
- methods
- inheritance
- relationships
- which methods belong to which classes

2. The SEQUENCE DIAGRAM defines:
- participants
- method-call order
- sender and receiver
- return messages
- ALT, LOOP, OPT and PAR fragments

Generate equivalent Python source code by combining information
from BOTH diagrams.

Important rules:
- Use the class diagram as the authoritative source for class structure
  and method ownership.
- Use the sequence diagram as the authoritative source for runtime behavior.
- Do not move methods to another class.
- Do not invent classes, methods, attributes or relationships.
- Preserve inheritance.
- Preserve ALT, LOOP, OPT and PAR control-flow semantics.
- If the sequence diagram contradicts the class diagram, preserve the
  class diagram structure and indicate the inconsistency with a Python comment.
- Return only valid Python source code without Markdown fences.

CLASS DIAGRAM XML:

{class_xml}

SEQUENCE DIAGRAM XML:

{sequence_xml}
"""

    print("Sending request to GEMMA...")

    return call_model(prompt)


def generate_from_files(
    class_xml_path,
    sequence_xml_path,
    output_path
):
    class_xml_path = Path(class_xml_path)
    sequence_xml_path = Path(sequence_xml_path)
    output_path = Path(output_path)

    class_xml = class_xml_path.read_text(encoding="utf-8")
    sequence_xml = sequence_xml_path.read_text(encoding="utf-8")

    print(f"Class XML size: {len(class_xml)} characters")
    print(f"Sequence XML size: {len(sequence_xml)} characters")

    generated_code = generate_python_from_xml(
        class_xml,
        sequence_xml
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated_code, encoding="utf-8")

    print()
    print("Generated code:")
    print(generated_code)
    print()
    print(f"Saved to: {output_path}")


BASE_DIR = Path(__file__).resolve().parent.parent


if __name__ == "__main__":
    generate_from_files(
        BASE_DIR / "diagrams" / "user-auth-class.drawio.xml",
        BASE_DIR / "diagrams" / "user-auth-sequence.drawio.xml",
        BASE_DIR / "outputs" / "ai_generated_output" / "nemotron_user_auth_class_sequence.py"
    )