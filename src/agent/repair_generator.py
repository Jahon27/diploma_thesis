from openai import OpenAI


def repair_code(
    client: OpenAI,
    model: str,
    class_model: str,
    sequence_model: str,
    generated_code: str,
    feedback: str,
) -> str:

    prompt = f"""
You are repairing Python code generated from UML diagrams.

The class diagram is the authoritative source for:
- classes
- attributes
- methods
- method ownership

The sequence diagram is the authoritative source for:
- participants
- method calls
- call order
- control-flow structures

Correct the previously generated Python code according to the
automatic evaluator feedback.

Rules:
- Preserve UML class names exactly.
- Preserve UML attribute names exactly.
- Preserve UML method names exactly.
- Do not rename identifiers.
- Do not invent classes, methods or attributes.
- Do not invent method calls.
- Preserve the sequence diagram call order.
- Preserve LOOP and ALT semantics.
- Correct every issue reported by the evaluator.
- Return only valid Python code.
- Do not use Markdown fences.
- Do not explain your answer.

CLASS MODEL:

{class_model}

SEQUENCE MODEL (SQD):

{sequence_model}

PREVIOUSLY GENERATED CODE:

{generated_code}

EVALUATOR FEEDBACK:

{feedback}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
    )

    if not response.choices:
        raise RuntimeError(
            f"Repair model returned no choices: {response}"
        )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Repair model returned an empty response."
        )

    return content