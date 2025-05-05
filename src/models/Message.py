from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Union, Optional, List
import json
import re

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


@dataclass
class Message:
    date: Optional[datetime] = field(default=None)
    author: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)
    characters: int = field(default=0)
    raw: Optional[str] = field(default=None)

    # only for stats
    responseOf: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.raw = self.raw

    def asJson(self) -> str:
        data: str = json.dumps(
            {
                "date": (
                    self.date.strftime(config["Formats"]["date"])
                    if not self.date is None else ""
                ),
                "author": self.author,
                "content": self.content,
            }
        )
        return data

    def asDict(self, datetimeAsString: bool = True) -> Dict[str, Union[datetime, str, None]]:
        data: Dict[str, Union[datetime, str, None]] = {
            "date": self.date,
            "author": self.author,
            "content": self.content,
        }

        if datetimeAsString:
            data["date"] = (
                self.date.strftime(config["Formats"]["date"])
                if not self.date is None else ""
            )

        return data

    def getDate(self, pattern: str, format: str) -> None:
        if not self.raw:
            raise ValueError("The raw message is required")

        search = re.search(pattern=pattern, string=self.raw)
        if not search:
            raise ValueError(
                f"Pattern{pattern} did not match any content for '{self.raw}'")
        date: str = search.group().replace(". ", "").replace(".", "")
        self.date = datetime.strptime(date, format)

    def getAuthor(self, pattern: str) -> None:
        if not self.raw:
            raise ValueError("The raw message is required")

        search = re.search(pattern=pattern, string=self.raw)
        if not search:
            raise ValueError(
                f"Pattern{pattern} did not match any content for '{self.raw}'")
        self.author = search.group().split(":")[0]

    def getContent(self, pattern: str) -> None:
        if not self.raw:
            raise ValueError("The raw message is required")

        search = re.search(pattern=pattern, string=self.raw)
        if not search:
            raise ValueError(
                f"Pattern{pattern} did not match any content for '{self.raw}'")
        self.content = search.group()

    def getCharacters(self):
        if not self.content:
            raise ValueError(
                "The content is required"
            )

        self.characters = len(self.content)
