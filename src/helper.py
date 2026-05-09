import re
import html
import xml.etree.ElementTree as ET

def clean_name(text: str) -> str:
    text = html.unescape(text or "").strip()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^a-zA-Z0-9_]", "_", text)
    text = re.sub(r"_+", "_", text)

    if not text:
        return "Unnamed"

    if text[0].isdigit():
        text = "_" + text

    return text

def to_class_name(name: str) -> str:
    name = clean_name(name)
    parts = [p for p in name.split("_") if p]
    return "".join(part[:1].upper() + part[1:] for part in parts) or "Unnamed"

def clean_text(text: str) -> str:
    return html.unescape(text or "").strip()

def parse_xml(xml_path: str) -> list[ET.Element]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cells = root.findall(".//mxCell")
    return cells

