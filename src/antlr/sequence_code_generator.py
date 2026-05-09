def make_result_var(method_name: str) -> str:
    return f"{method_name}_result"


def emit_message(msg: dict, indent: int = 1) -> list[str]:
    lines = []
    prefix = "    " * indent

    if msg["type"] == "call":
        lines.append(f"{prefix}{msg['to']}.{msg['method']}()")

    elif msg["type"] == "self":
        lines.append(f"{prefix}{msg['object']}.{msg['method']}()")

    elif msg["type"] == "alt":
        condition = msg["condition"]

        lines.append(f"{prefix}if {condition}:")
        if msg["then"]:
            for inner_msg in msg["then"]:
                lines.extend(emit_message(inner_msg, indent + 1))
        else:
            lines.append(f"{prefix}    pass")

        if msg["else"]:
            lines.append(f"{prefix}else:")
            for inner_msg in msg["else"]:
                lines.extend(emit_message(inner_msg, indent + 1))

    elif msg["type"] == "loop":
        condition = msg["condition"]

        lines.append(f"{prefix}while {condition}:")
        if msg["body"]:
            for inner_msg in msg["body"]:
                lines.extend(emit_message(inner_msg, indent + 1))
        else:
            lines.append(f"{prefix}    pass")

    return lines


def generate_sequence_code(model: dict) -> str:
    lines = []

    participants = model["participants"]
    messages = model["messages"]

    lines.append("def run_sequence():")

    if not participants:
        lines.append("    pass")
        return "\n".join(lines)

    for var_name, class_name in participants.items():
        lines.append(f"    {var_name} = {class_name}()")

    lines.append("")

    for msg in messages:
        if msg["type"] == "return":
            continue

        lines.extend(emit_message(msg, indent=1))

    return "\n".join(lines)