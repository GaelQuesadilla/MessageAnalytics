from src.models.Chat import Chat
from typing import List, Dict, Union
from datetime import datetime
import matplotlib.pyplot as plt


class AllMessages():
    def __init__(self, chat: Chat):
        self.chat: Chat = chat
        self.dates: List[datetime] = []
        self.messages: List[int] = []
        self.messagesByAuthor: Dict[Union[str, None], List[int]] = {}

    def process(self):
        msgGroupedByDate = self.chat.getMessagesGroupedByDate(
            untilToday=False
        )
        msgGroupedByDateAndAuthor = self.chat.getMessagesGroupedByDateAndAuthor(
            untilToday=False
        )

        self.chat.messages = []

        self.dates = msgGroupedByDate.keys()

        self.messages = [len(msgs) for date, msgs in msgGroupedByDate.items()]
        self.messagesByAuthor = {
            author:
                [
                    len(msgsByAuth.get(author)) for date, msgsByAuth
                    in msgGroupedByDateAndAuthor.items()
                ]
            for author in [author.name for author in self.chat.authors]}

    def show(self):
        fig, ax = plt.subplots()

        ax.plot_date(
            self.dates,
            self.messages,
            label="Total",
            marker="",
            linestyle="-"
        )
        for author in [author.name for author in self.chat.authors]:
            if author == "Provider":
                continue
            ax.plot_date(
                self.dates,
                self.messagesByAuthor.get(author),
                label=author,
                marker="",
                linestyle="-"
            )

        ax.legend()
        fig.autofmt_xdate()
        plt.show()
