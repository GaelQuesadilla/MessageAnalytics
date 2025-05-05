from src.models.Chat import Chat
from typing import List, Dict
from src.models.Author import Author
from src.models.Message import Message
from alive_progress import alive_bar
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from math import log2
from src.utils.prettyDelta import prettyDelta


class ChatStats(Chat):

    def getResponses(self) -> List[Message]:
        currentAuthor: str = None
        responses: List[Message] = []
        for message in self.messages:
            if message.author == "Provider":
                continue
            if message.author == currentAuthor:
                continue

            currentAuthor = message.author
            responses.append(message)

        newChat = Chat()
        newChat.messages = responses

        with open("./data/output/data.json", "w") as file:
            file.write(newChat.asJson())

        return responses

    def getResponseTime(self) -> Dict[str, List[int]]:
        responses = self.getResponses()
        authors: Dict[List[int]] = {
            author.name: []
            for author in self.authors if not author.name is None
        }

        for res in responses:
            res.responseOf = []

        currentAuthor: str
        with alive_bar(len(responses)) as bar:
            for i, res in enumerate(responses):
                currentAuthor = res.author
                for author in authors:
                    if author == currentAuthor:
                        continue

                    nextResponses = responses[i::]

                    for nextRes in nextResponses:
                        if author in nextRes.responseOf:
                            break
                        if not author == nextRes.author:
                            continue

                        nextRes.responseOf.append(author)

                        deltaTime: timedelta = nextRes.date - res.date

                        authors[author].append(
                            deltaTime.total_seconds()
                        )

                        break

                bar()

        return authors

    def getFrequencyTable(self, author: str, precision: int = 2) -> pd.Series:

        data = self.getResponseTime().get(author)
        if data is None:
            raise ValueError(f"Author {author} not in self.authors")

        arr = np.array(data, dtype=float)
        n = arr.size

        cuts = np.asarray(
            [
                0,
                120,
                600,
                1800,
                7200,
                21600,
                86400,
                259200,
                604800,
                1296000,
                2592000,
                7776000,
                15552000,
                31536000,
                max(63072000, arr.max())
            ],
            dtype=float
        )

        categories = pd.cut(arr, bins=cuts, precision=precision, right=False)

        freq = categories.value_counts()
        freq_rel = freq / n
        freq_acum = freq.cumsum()
        freq_rel_acum = freq_rel.cumsum()

        def prettyInterval(left, right):
            return f"{prettyDelta(left)} - {prettyDelta(right)}"

        df = pd.DataFrame({
            'Intervalo': [
                prettyInterval(iv.left, iv.right)
                for iv in freq.index
            ],
            # 'Límite Inferior': [iv.left for iv in freq.index],
            # 'Límite Superior': [iv.right for iv in freq.index],
            # 'Marca de Clase': [(iv.left + iv.right) / 2 for iv in freq.index],
            'Frecuencia': freq.values,
            'Frecuencia Relativa': np.round(freq_rel.values, precision),
            'Frecuencia Acumulada': freq_acum.values,
            'Frecuencia Relativa Acumulada': np.round(freq_rel_acum.values, precision),
        })

        return df
