from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FormOption:
    value: str
    label: str


@dataclass
class FormField:
    tag: str
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    placeholder: Optional[str]
    aria_label: Optional[str]
    text: Optional[str]
    options: Optional[List[FormOption]] = None
