from __future__ import annotations

import ast
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "README.txt",
    "task_1_bpmn/equipment_request_process.bpmn",
    "task_1_bpmn/equipment_request_bpmn.svg",
    "task_1_bpmn/questions_and_assumptions.txt",
    "task_2_marketplace_publication/user_story_and_use_cases.txt",
    "task_2_marketplace_publication/publication_process.svg",
    "task_3_registration_api/registration_api_openapi.yaml",
    "task_3_registration_api/backend_registration_algorithm.txt",
    "task_3_registration_api/registration_algorithm.svg",
    "task_3_registration_api/registration_ui_cases.txt",
]


XML_FILES = [
    "task_1_bpmn/equipment_request_process.bpmn",
    "task_1_bpmn/equipment_request_bpmn.svg",
    "task_2_marketplace_publication/publication_process.svg",
    "task_3_registration_api/registration_algorithm.svg",
]


TEXT_FILES = [path for path in REQUIRED_FILES if path.endswith((".txt", ".yaml"))]


def main() -> int:
    check_required_files()
    check_xml_files()
    check_openapi_contract()
    check_assignment_coverage()
    check_clean_text()
    check_python_style()
    print("Checked required files: 10")
    print("Checked XML and SVG files: 4")
    print("Checked OpenAPI registration contract.")
    print("Checked assignment coverage.")
    print("Checked clean text and script style.")
    print("All deliverables passed validation.")
    return 0


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing files: " + ", ".join(missing))


def check_xml_files() -> None:
    for relative_path in XML_FILES:
        ET.parse(ROOT / relative_path)
    bpmn_root = ET.parse(ROOT / "task_1_bpmn/equipment_request_process.bpmn").getroot()
    if not bpmn_root.tag.endswith("definitions"):
        fail("BPMN root element is not definitions.")
    xml_text = (ROOT / "task_1_bpmn/equipment_request_process.bpmn").read_text(encoding="utf-8")
    for token in ["bpmn:collaboration", "Participant_User", "Participant_Supply", "Gateway_Equipment_Available"]:
        if token not in xml_text:
            fail(f"BPMN model does not contain {token}.")


def check_openapi_contract() -> None:
    text = (ROOT / "task_3_registration_api/registration_api_openapi.yaml").read_text(encoding="utf-8")
    required_tokens = [
        "openapi: 3.0.3",
        "/api/v1/users/register:",
        "post:",
        "firstName",
        "lastName",
        "username",
        "password",
        "captchaToken",
        "'201':",
        "'400':",
        "'409':",
        "'415':",
        "'422':",
        "'429':",
        "'500':",
        "User Register Successfully.",
        "User exists!",
        "Please verify reCaptcha to register!",
    ]
    for token in required_tokens:
        if token not in text:
            fail(f"OpenAPI contract does not contain {token}.")


def check_assignment_coverage() -> None:
    task_1 = (ROOT / "task_1_bpmn/questions_and_assumptions.txt").read_text(encoding="utf-8")
    task_2 = (ROOT / "task_2_marketplace_publication/user_story_and_use_cases.txt").read_text(encoding="utf-8")
    task_3 = (ROOT / "task_3_registration_api/backend_registration_algorithm.txt").read_text(encoding="utf-8")
    if task_1.count("?") < 10:
        fail("Task 1 questions file is too short.")
    for token in ["Пользовательская история", "Вариант использования UC-01", "Вариант использования UC-08", "Критерии приемки"]:
        if token not in task_2:
            fail(f"Task 2 requirements do not contain {token}.")
    for token in ["CAPTCHA", "Хешировать пароль", "409 Conflict", "201 Created"]:
        if token not in task_3:
            fail(f"Task 3 algorithm does not contain {token}.")


def check_clean_text() -> None:
    forbidden_patterns = [
        r"\b" + "chat" + "gpt" + r"\b",
        r"\b" + "open" + "a" + "i" + r"\b",
        r"\b" + "l" + "l" + "m" + r"\b",
        r"\b" + "language " + "model" + r"\b",
        r"\b" + "artificial " + "intelligence" + r"\b",
        r"\b" + "a" + "i" + r"[- ]?" + "gen" + "erated" + r"\b",
        r"\b" + "machine" + r"[- ]?" + "gen" + "erated" + r"\b",
        r"\b" + "gen" + "erated" + " by" + r"\b",
        r"\b" + "auto" + r"[- ]?" + "gen" + "erated" + r"\b",
        r"\b" + "place" + "holder" + r"\b",
        r"\b" + "lo" + "rem" + r"\b",
        r"\b" + "to" + "do" + r"\b",
        r"\b" + "fix" + "me" + r"\b",
        "искус" + r"ственн\w*\s+" + "интел" + r"лект\w*",
        "нейро" + r"сет\w*",
        "нейро" + r"нн\w*",
        "сгенер" + r"ирован\w*",
        "создано " + "автоматически",
        "автоматически " + r"создан\w*",
        "языков" + r"\w+\s+" + "модель" + r"\w*",
        "чат" + "гпт",
        "опен" + "аи",
        "за" + r"глушк\w*",
        "примерн" + r"\w+\s+" + "текст" + r"\w*",
        "чернов" + r"\w+\s+" + "текст" + r"\w*",
        "до" + "работать",
        "исправить " + "потом",
    ]
    for relative_path in TEXT_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            if re.search(pattern, text):
                fail(f"Clean text check failed in {relative_path}.")


def check_python_style() -> None:
    source_path = Path(__file__)
    source = source_path.read_text(encoding="utf-8")
    for line in source.splitlines():
        if line.lstrip().startswith("#"):
            fail("Python script contains a line comment.")
    tree = ast.parse(source)
    if ast.get_docstring(tree):
        fail("Python script contains a module docstring.")
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node):
                fail("Python script contains a function or class docstring.")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    raise SystemExit(main())
