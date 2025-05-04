from dataclasses import dataclass, field
from typing import Optional, Dict, Union


@dataclass
class Author:
    inChat: bool = field(default=True)
    messages: int = field(default=0)
    name: Optional[str] = field(default=None),

    def asDict(self) -> Dict[str, Union[bool, int, str, None]]:
        return {
            "inChat": self.inChat,
            "messages": self.messages,
            "name": self.name,
        }
