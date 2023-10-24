import json
from typing import Dict


async def reverse_text(text: str) -> Dict[str, str]:
    reversed_text = text[::-1]
    return json.dumps({'reversed_text': reversed_text}, ensure_ascii=False)
