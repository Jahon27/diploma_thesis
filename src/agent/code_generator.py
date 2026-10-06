from openai import OpenAI


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

    return response.choices[0].message.content