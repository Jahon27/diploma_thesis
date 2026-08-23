import ast
import re
from pathlib import Path
from typing import Any


def load_python_file(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_python(code: str):
    try:
        return ast.parse(code), None
    except SyntaxError as exc:
        return None, str(exc)


def extract_classes(tree: ast.AST) -> set[str]:
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }


def extract_methods(tree: ast.AST) -> dict[str, set[str]]:
    result = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        result[node.name] = {
            child.name
            for child in node.body
            if isinstance(
                child,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        }

    return result


def extract_attributes(tree: ast.AST) -> dict[str, set[str]]:
    result = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        attributes = set()

        for child in node.body:
            if not isinstance(child, ast.FunctionDef):
                continue

            if child.name != "__init__":
                continue

            for subnode in ast.walk(child):

                if isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id == "self"
                        ):
                            attributes.add(target.attr)

                elif isinstance(subnode, ast.AnnAssign):
                    target = subnode.target

                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        attributes.add(target.attr)

        result[node.name] = attributes

    return result


def find_run_function(tree: ast.AST) -> ast.FunctionDef | None:
    preferred_names = {
        "run_sequence",
        "run_checkout_process",
        "execute_checkout_process",
        "main",
    }

    for node in tree.body:
        if (
            isinstance(node, ast.FunctionDef)
            and node.name in preferred_names
        ):
            return node

    return None


def receiver_to_string(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        left = receiver_to_string(node.value)

        if left:
            return f"{left}.{node.attr}"

        return node.attr

    return "unknown"


class CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            receiver = receiver_to_string(node.func.value)
            method = node.func.attr

            self.calls.append(
                f"{receiver}.{method}"
            )

        self.generic_visit(node)


def extract_call_sequence(tree: ast.AST) -> list[str]:
    function = find_run_function(tree)

    if function is None:
        return []

    visitor = CallVisitor()
    visitor.visit(function)

    return visitor.calls


def extract_control_flow(tree: ast.AST) -> dict[str, int]:
    function = find_run_function(tree)

    if function is None:
        return {
            "if": 0,
            "while": 0,
            "for": 0,
        }

    return {
        "if": sum(
            isinstance(node, ast.If)
            for node in ast.walk(function)
        ),
        "while": sum(
            isinstance(node, ast.While)
            for node in ast.walk(function)
        ),
        "for": sum(
            isinstance(node, ast.For)
            for node in ast.walk(function)
        ),
    }


def extract_conditions(tree: ast.AST) -> list[str]:
    function = find_run_function(tree)

    if function is None:
        return []

    conditions = []

    for node in ast.walk(function):

        if isinstance(node, ast.If):
            conditions.append(
                f"if {ast.unparse(node.test)}"
            )

        elif isinstance(node, ast.While):
            conditions.append(
                f"while {ast.unparse(node.test)}"
            )

        elif isinstance(node, ast.For):
            conditions.append(
                f"for {ast.unparse(node.target)} in "
                f"{ast.unparse(node.iter)}"
            )

    return conditions


def flatten_methods(
    methods: dict[str, set[str]]
) -> set[str]:
    return {
        f"{class_name}.{method}"
        for class_name, class_methods in methods.items()
        for method in class_methods
    }


def flatten_attributes(
    attributes: dict[str, set[str]]
) -> set[str]:
    return {
        f"{class_name}.{attribute}"
        for class_name, class_attributes in attributes.items()
        for attribute in class_attributes
    }


def compare_sets(
    reference: set[str],
    candidate: set[str]
) -> dict[str, Any]:

    correct = reference & candidate
    missing = reference - candidate
    extra = candidate - reference

    recall = (
        len(correct) / len(reference)
        if reference
        else 1.0
    )

    precision = (
        len(correct) / len(candidate)
        if candidate
        else 1.0
    )

    return {
        "reference_count": len(reference),
        "candidate_count": len(candidate),
        "correct_count": len(correct),

        "precision": round(precision, 4),
        "recall": round(recall, 4),

        "missing": sorted(missing),
        "extra": sorted(extra),
    }


def normalize_identifier(name: str) -> str:
    """
    customerId -> customerid
    customer_id -> customerid

    Used only to detect renaming.
    """
    return re.sub(r"[^a-zA-Z0-9]", "", name).lower()


def split_qualified_name(value: str) -> tuple[str, str]:
    class_name, member = value.split(".", 1)
    return class_name, member


def compare_attributes(
    reference: set[str],
    candidate: set[str]
) -> dict[str, Any]:

    exact_correct = reference & candidate
    missing = set(reference - candidate)
    extra = set(candidate - reference)

    renamed = []

    consumed_missing = set()
    consumed_extra = set()

    for ref in missing:
        ref_class, ref_attr = split_qualified_name(ref)

        for cand in extra:
            cand_class, cand_attr = split_qualified_name(cand)

            if ref_class != cand_class:
                continue

            if (
                normalize_identifier(ref_attr)
                == normalize_identifier(cand_attr)
            ):
                renamed.append({
                    "reference": ref,
                    "candidate": cand
                })

                consumed_missing.add(ref)
                consumed_extra.add(cand)
                break

    true_missing = missing - consumed_missing
    invented = extra - consumed_extra

    structurally_correct = (
        len(exact_correct)
        + len(renamed)
    )

    recall = (
        structurally_correct / len(reference)
        if reference
        else 1.0
    )

    precision = (
        structurally_correct / len(candidate)
        if candidate
        else 1.0
    )

    exact_recall = (
        len(exact_correct) / len(reference)
        if reference
        else 1.0
    )

    return {
        "reference_count": len(reference),
        "candidate_count": len(candidate),

        "exact_correct_count": len(exact_correct),
        "renamed_count": len(renamed),

        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "exact_name_recall": round(exact_recall, 4),

        "renamed": renamed,
        "missing": sorted(true_missing),
        "invented": sorted(invented),
    }


def compare_calls(
    reference: list[str],
    candidate: list[str]
) -> dict[str, Any]:

    reference_set = set(reference)
    candidate_set = set(candidate)

    correct = reference_set & candidate_set
    missing = reference_set - candidate_set
    extra = candidate_set - reference_set

    recall = (
        len(correct) / len(reference_set)
        if reference_set
        else 1.0
    )

    precision = (
        len(correct) / len(candidate_set)
        if candidate_set
        else 1.0
    )

    exact_order_match = reference == candidate

    return {
        "reference_count": len(reference_set),
        "candidate_count": len(candidate_set),
        "correct_count": len(correct),

        "precision": round(precision, 4),
        "recall": round(recall, 4),

        "missing": sorted(missing),
        "extra": sorted(extra),

        "exact_order_match": exact_order_match,
        "reference_order": reference,
        "candidate_order": candidate,
    }


def compare_control_flow(
    reference: dict[str, int],
    candidate: dict[str, int]
) -> dict[str, Any]:

    keys = {"if", "while", "for"}

    differences = {
        key: candidate.get(key, 0) - reference.get(key, 0)
        for key in keys
    }

    exact_match = all(
        reference.get(key, 0)
        == candidate.get(key, 0)
        for key in keys
    )

    return {
        "exact_match": exact_match,
        "reference": reference,
        "candidate": candidate,
        "difference": differences,
    }


def calculate_f1(
    precision: float,
    recall: float
) -> float:

    if precision + recall == 0:
        return 0.0

    return (
        2 * precision * recall
        / (precision + recall)
    )


def calculate_fidelity_score(
    classes: dict,
    methods: dict,
    attributes: dict,
    calls: dict,
    control_flow: dict
) -> dict[str, float]:

    class_f1 = calculate_f1(
        classes["precision"],
        classes["recall"]
    )

    method_f1 = calculate_f1(
        methods["precision"],
        methods["recall"]
    )

    attribute_f1 = calculate_f1(
        attributes["precision"],
        attributes["recall"]
    )

    call_f1 = calculate_f1(
        calls["precision"],
        calls["recall"]
    )

    control_flow_score = (
        1.0
        if control_flow["exact_match"]
        else 0.0
    )

    # Same weight for the first version.
    overall = (
        class_f1
        + method_f1
        + attribute_f1
        + call_f1
        + control_flow_score
    ) / 5

    return {
        "class_f1": round(class_f1, 4),
        "method_f1": round(method_f1, 4),
        "attribute_f1": round(attribute_f1, 4),
        "call_f1": round(call_f1, 4),
        "control_flow_score": round(
            control_flow_score,
            4
        ),
        "overall_uml_fidelity": round(
            overall,
            4
        ),
    }


def extract_model(tree: ast.AST) -> dict[str, Any]:

    methods = extract_methods(tree)
    attributes = extract_attributes(tree)

    return {
        "classes": extract_classes(tree),
        "methods": flatten_methods(methods),
        "attributes": flatten_attributes(attributes),
        "calls": extract_call_sequence(tree),
        "control_flow": extract_control_flow(tree),
        "conditions": extract_conditions(tree),
    }


def evaluate(
    reference_path: str | Path,
    candidate_path: str | Path
) -> dict[str, Any]:

    reference_code = load_python_file(reference_path)
    candidate_code = load_python_file(candidate_path)

    reference_tree, reference_error = parse_python(
        reference_code
    )

    candidate_tree, candidate_error = parse_python(
        candidate_code
    )

    if reference_error:
        raise RuntimeError(
            f"Reference code is invalid: {reference_error}"
        )

    if candidate_error:
        return {
            "syntax_valid": False,
            "syntax_error": candidate_error,
            "uml_fidelity": {
                "overall_uml_fidelity": 0.0
            }
        }

    reference = extract_model(reference_tree)
    candidate = extract_model(candidate_tree)

    classes_result = compare_sets(
        reference["classes"],
        candidate["classes"]
    )

    methods_result = compare_sets(
        reference["methods"],
        candidate["methods"]
    )

    attributes_result = compare_attributes(
        reference["attributes"],
        candidate["attributes"]
    )

    calls_result = compare_calls(
        reference["calls"],
        candidate["calls"]
    )

    control_flow_result = compare_control_flow(
        reference["control_flow"],
        candidate["control_flow"]
    )

    fidelity = calculate_fidelity_score(
        classes_result,
        methods_result,
        attributes_result,
        calls_result,
        control_flow_result
    )

    return {
        "syntax_valid": True,

        "classes": classes_result,
        "methods": methods_result,
        "attributes": attributes_result,
        "calls": calls_result,

        "control_flow": control_flow_result,

        "reference_conditions":
            reference["conditions"],

        "candidate_conditions":
            candidate["conditions"],

        "uml_fidelity": fidelity,
    }