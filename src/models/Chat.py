from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Set, Union, Dict, Optional
from src.models.Message import Message
import json
import configparser
from src.utils.normalize import normalize
from datetime import datetime, timedelta
from alive_progress import alive_bar
import re
from collections import Counter

config = configparser.ConfigParser()
config.read("config.ini")


@dataclass
class Chat:
    file: Optional[Path] = field(default=None)
    messages: List[Message] = field(default_factory=list)
    authors: Set[Union[str, None]] = field(default_factory=set)

    def asJson(self):
        return json.dumps([message.asDict(datetimeAsString=True) for message in self.messages])

    def addMessage(self, message: Message) -> None:
        self.messages.append(message)
        self.authors.add(message.author)

    def getAuthorMessages(self, author: Union[str, None]) -> List[Message]:
        return [msg for msg in self.messages if msg.author == author]

    def getMessagesGroupedByDate(self, untilToday: bool) -> Dict[datetime, List[Message]]:
        startDate = self.messages[0].date
        if untilToday:
            endDate = datetime.now()
        else:
            endDate = self.messages[-1].date

        startDate = datetime(
            year=startDate.year, month=startDate.month, day=startDate.day)
        endDate = datetime(
            year=endDate.year, month=endDate.month, day=endDate.day)

        delta = endDate - startDate

        dates = [startDate + timedelta(days=1)
                 * i for i in range(delta.days + 1)]

        tmpMessages = self.messages.copy()
        messagesGroupedByDate: Dict[datetime, List[Message]] = {
            date: [] for date in dates
        }

        while len(tmpMessages) > 0:
            currentMessage = tmpMessages[-1]

            currentDate = datetime(
                year=currentMessage.date.year,
                month=currentMessage.date.month,
                day=currentMessage.date.day
            )

            messagesGroupedByDate[currentDate].append(currentMessage)

            tmpMessages.pop()

        return messagesGroupedByDate

    def getMessagesGroupedByDateAndAuthor(self, untilToday: bool) -> Dict[datetime, Dict[Union[str, None], List[Message]]]:
        startDate = self.messages[0].date
        if untilToday:
            endDate = datetime.now()
        else:
            endDate = self.messages[-1].date

        startDate = datetime(
            year=startDate.year, month=startDate.month, day=startDate.day)
        endDate = datetime(
            year=endDate.year, month=endDate.month, day=endDate.day)

        delta = endDate - startDate

        dates = [startDate + timedelta(days=1)
                 * i for i in range(delta.days + 1)]

        tmpMessages = self.messages.copy()
        messagesGroupedByDateAndAuthor: Dict[datetime, Dict[Union[str, None], List[str]]] = {
            date: {author: [] for author in self.authors} for date in dates
        }

        messagesGroupedByDateAndAuthor: Dict[
            datetime, Dict[Union[str, None], List[str]]
        ] = {}

        for date in dates:
            messagesGroupedByDateAndAuthor[date] = {}
            for author in self.authors:
                messagesGroupedByDateAndAuthor[date][author] = []

        while len(tmpMessages) > 0:
            currentMessage = tmpMessages[-1]

            currentDate = datetime(
                year=currentMessage.date.year,
                month=currentMessage.date.month,
                day=currentMessage.date.day
            )

            messagesGroupedByDateAndAuthor[currentDate][currentMessage.author].append(
                currentMessage)

            tmpMessages.pop()

        return messagesGroupedByDateAndAuthor

    def stats(self) -> Dict[str, Union[int, Dict[Union[str, None], int]]]:
        return {
            "TotalMessages": len(self.messages),
            "TotalAuthors": len(self.authors),
            "MessagesByAuthor": {
                author: len(self.getAuthorMessages(author)) for author in self.authors
            }

        }

    def loadFromFile(self):
        if not self.file.exists():
            raise FileNotFoundError(f"The file {self.file} does not exist")

        with self.file.open(encoding="UTF-8") as file:
            raws = file.readlines()
        with alive_bar(len(raws)) as bar:
            for index, raw in enumerate(raws):
                message = Message(raw=normalize(raw))

                try:
                    message.getDate(
                        pattern=config["Patterns"]["date"],
                        format=config["Formats"]["date"],
                    )
                except:
                    self.messages[-1].content += normalize(raw)
                    bar()
                    continue
                try:
                    message.getAuthor(
                        pattern=config["Patterns"]["author"]
                    )
                    message.getContent(
                        pattern=config["Patterns"]["content"]
                    )
                except ValueError:
                    message.author = "Provider"
                    message.getContent(
                        pattern=config["Patterns"]["contentWhenProvider"]
                    )

                self.addMessage(message=message)
                message.raw = ""
                bar()

    def getWorldFrec(self) -> Counter:
        content: List[str] = [
            msg.content for msg in self.messages if msg.content]
        cleanContent: List[str] = [
            re.sub(r"[^\w\s]", "", message.lower())
            for message in content
        ]

        words: List[str] = [
            word for message in cleanContent for word in message.split()

        ]

        del content
        del cleanContent

        worldFrec: Counter = Counter(words)
        return worldFrec
