def emit_message(msg: dict, indent: int = 1) -> list[str]:
    lines = []
    prefix = "    " * indent

    if msg["type"] == "call":
        lines.append(
            f"{prefix}{msg['to']}.{msg['method']}()"
        )

    elif msg["type"] == "self":
        lines.append(
            f"{prefix}{msg['object']}.{msg['method']}()"
        )

    elif msg["type"] == "return":
        # Return messages represent information flow,
        # not a separate Python method invocation.
        pass

    elif msg["type"] == "alt":
        condition = msg["condition"]

        lines.append(f"{prefix}if {condition}:")

        if msg["then"]:
            for inner_msg in msg["then"]:
                lines.extend(
                    emit_message(inner_msg, indent + 1)
                )
        else:
            lines.append(f"{prefix}    pass")

        if msg["else"]:
            lines.append(f"{prefix}else:")

            for inner_msg in msg["else"]:
                lines.extend(
                    emit_message(inner_msg, indent + 1)
                )

    elif msg["type"] == "loop":
        condition = msg["condition"]

        lines.append(f"{prefix}while {condition}:")

        if msg["body"]:
            for inner_msg in msg["body"]:
                lines.extend(
                    emit_message(inner_msg, indent + 1)
                )
        else:
            lines.append(f"{prefix}    pass")

    return lines


def collect_conditions(messages: list[dict]) -> list[str]:
    conditions = []

    def add_condition(condition: str):
        if condition not in conditions:
            conditions.append(condition)

    for msg in messages:
        if msg["type"] == "alt":
            add_condition(msg["condition"])

            conditions.extend(
                condition
                for condition in collect_conditions(msg["then"])
                if condition not in conditions
            )

            conditions.extend(
                condition
                for condition in collect_conditions(msg["else"])
                if condition not in conditions
            )

        elif msg["type"] == "loop":
            add_condition(msg["condition"])

            conditions.extend(
                condition
                for condition in collect_conditions(msg["body"])
                if condition not in conditions
            )

    return conditions


def generate_sequence_code(model: dict) -> str:
    lines = []

    participants = model["participants"]
    messages = model["messages"]

    conditions = collect_conditions(messages)

    # Conditions become function parameters instead of
    # being artificially initialized to False.
    params = ", ".join(conditions)

    if params:
        lines.append(f"def run_sequence({params}):")
    else:
        lines.append("def run_sequence():")

    if not participants:
        lines.append("    pass")
        return "\n".join(lines)

    for var_name, class_name in participants.items():
        lines.append(
            f"    {var_name} = {class_name}()"
        )

    if messages:
        lines.append("")

    for msg in messages:
        lines.extend(
            emit_message(msg, indent=1)
        )

    return "\n".join(lines)