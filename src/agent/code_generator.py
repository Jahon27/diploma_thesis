from openai import OpenAI
from agent.code_cleaner import clean_generated_code

def generate_code(
    client: OpenAI,
    model: str,
    class_model: str,
    sequence_model: str,
) -> str:

    prompt = f"""
You are generating Python source code from UML diagrams.

The CLASS MODEL is the authoritative source for:
- classes
- attributes
- methods
- method ownership
- inheritance

The SEQUENCE MODEL (SQD) is the authoritative source for:
- participants
- method calls
- return messages
- call order
- control-flow structures
- control-flow conditions

Generate Python code that faithfully implements both models.

SQD semantics:
- "participant variable ClassName" defines an object variable and its class.
- "call sender receiver method" means the sender invokes method on the receiver.
  Generate this as: receiver.method()
- Example:
  "call order inventory reserveProduct"
  means:
  inventory.reserveProduct()
  NOT:
  order.inventory.reserveProduct()
- "self receiver method" means:
  receiver.method()
- "return sender receiver value" represents a return message.
  Do not convert it into an additional method call.
- "loop condition" represents repeated execution controlled by that condition.
- "alt condition" represents a conditional branch.
- "else condition" represents the alternative branch.

Rules:
- Preserve all class names exactly.
- Preserve all attribute names exactly.
- Preserve all method names exactly.
- Place methods in their correct classes.
- Do not invent classes.
- Do not invent attributes.
- Do not invent methods.
- Do not invent method calls.
- Preserve the sequence call order.
- Preserve LOOP and ALT semantics.
- Represent the sequence behavior in executable Python.
- The result must be syntactically valid Python.
- Return only Python source code.
- Do not use Markdown fences.
- Do not explain the result.

MANDATORY PYTHON OUTPUT STRUCTURE:

Generate ONE complete, self-contained Python module.

PART 1 — CLASS DEFINITIONS:
- Generate every class specified in the CLASS MODEL.
- Define all classes at the top level of the module.
- Preserve the exact class names.
- Preserve every UML attribute and method.
- Implement __init__ to initialize UML attributes using self.attribute.
- Keep methods inside their corresponding classes.
- If a UML method has no specified behavior, use pass.
- Do not omit any UML class, attribute, or method.
- Do not define classes inside run_sequence.
- Do not import UML classes from external modules.

PART 2 — SEQUENCE IMPLEMENTATION:
- After all class definitions, define a top-level
  function named run_sequence.
- Create the UML participant objects inside run_sequence.
- Execute UML method calls inside run_sequence.
- Preserve the exact receiver.method() format from SQD.
- Preserve the exact order of calls.
- Translate UML loop fragments into Python while loops.
- Translate UML alt fragments into Python if/else statements,
  only when present in the SEQUENCE MODEL.
- Preserve UML conditions exactly when valid Python.
- Pass external condition variables as function parameters
  rather than inventing constant values.
- Do not invent statements that force a loop to terminate.
- Do not execute run_sequence automatically.

CRITICAL REQUIREMENTS:
- The output MUST include BOTH parts.
- Never return only the classes.
- Never return only run_sequence.
- Return the complete Python file, not a code fragment.
- All UML classes must be defined before run_sequence.
- Return only syntactically valid Python source code.
- Do not include Markdown fences or explanations.

CLASS MODEL:

{class_model}

SEQUENCE MODEL (SQD):

{sequence_model}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    if not response.choices:
        raise RuntimeError(
            f"Generation model returned no choices: {response}"
        )

    return clean_generated_code(response.choices[0].message.content)