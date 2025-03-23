from typing import List, Dict


def normalize(value: str) -> str:
    replacements: Dict[str, List[str]] = {
        " ": [" ", "â€¯"]
    }

    for target, chars in replacements.items():
        for char in chars:
            value = value.replace(char, target)

    return value
