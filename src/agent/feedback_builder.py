def build_feedback(evaluation: dict) -> str:
    if not evaluation["syntax_valid"]:
        return (
            "The generated Python code is syntactically invalid.\n"
            f"Syntax error: {evaluation['syntax_error']}\n\n"
            "Fix the syntax while preserving the UML structure exactly."
        )

    problems = []

    # Classes
    for value in evaluation["classes"]["missing"]:
        problems.append(f"Missing class: {value}")

    for value in evaluation["classes"]["extra"]:
        problems.append(f"Invented class: {value}")

    # Methods
    for value in evaluation["methods"]["missing"]:
        problems.append(f"Missing method: {value}")

    for value in evaluation["methods"]["extra"]:
        problems.append(f"Invented method: {value}")

    # Attributes
    for value in evaluation["attributes"]["missing"]:
        problems.append(f"Missing attribute: {value}")

    for value in evaluation["attributes"]["invented"]:
        problems.append(f"Invented attribute: {value}")

    for renamed in evaluation["attributes"]["renamed"]:
        problems.append(
            f"Renamed attribute: "
            f"{renamed['candidate']} should be "
            f"{renamed['reference']}"
        )

    # Calls
    for value in evaluation["calls"]["missing"]:
        problems.append(f"Missing sequence call: {value}()")

    for value in evaluation["calls"]["extra"]:
        problems.append(f"Invented sequence call: {value}()")

    if not evaluation["calls"]["exact_order_match"]:
        problems.append(
            "Method-call order does not match the sequence diagram.\n"
            f"Expected: {evaluation['calls']['reference_order']}\n"
            f"Generated: {evaluation['calls']['candidate_order']}"
        )

    # Control flow
    if not evaluation["control_flow"]["exact_match"]:
        problems.append(
            "Control-flow structure does not match the sequence diagram.\n"
            f"Expected: {evaluation['control_flow']['reference']}\n"
            f"Generated: {evaluation['control_flow']['candidate']}"
        )

    # Conditions
    if (
        evaluation["reference_conditions"]
        != evaluation["candidate_conditions"]
    ):
        problems.append(
            "Control-flow conditions do not match.\n"
            f"Expected: {evaluation['reference_conditions']}\n"
            f"Generated: {evaluation['candidate_conditions']}"
        )

    if not problems:
        return "No UML fidelity problems detected."

    return (
        "The generated Python code does not faithfully match the UML.\n\n"
        + "\n".join(f"- {problem}" for problem in problems)
        + "\n\nCorrect all listed problems. "
          "Do not invent any elements that are absent from the UML."
    )