from openai import OpenAI
from agent.code_cleaner import clean_generated_code

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

SEQUENCE IMPLEMENTATION RULES:
- Implement the UML sequence diagram inside a top-level
  Python function named run_sequence.
- Create all sequence participant objects inside run_sequence.
- Preserve the exact order of UML method calls.
- Translate UML "loop" fragments into Python while loops.
- Translate UML "alt" fragments into Python if/else statements,
  but only if they exist in the sequence model.
- Preserve the original loop and alternative conditions.
- Do not invent loop termination statements such as
  "eachOrderItem = False".
- Do not place sequence execution statements at module level.
- Do not automatically execute run_sequence.
- Return only valid Python source code.

MANDATORY REPAIR OUTPUT:
- Return the COMPLETE corrected Python module.
- Include EVERY class from the CLASS MODEL.
- Include all UML attributes and methods.
- Define classes at module level.
- Include a top-level run_sequence function.
- Include every required UML sequence call.
- Preserve UML call order and control-flow conditions.
- Preserve correct code while repairing incorrect code.
- Never remove correct classes to repair the sequence.
- Never remove the sequence to repair class definitions.
- Never return only the modified fragment.
- Never invent additional UML elements.


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

    return clean_generated_code(content)