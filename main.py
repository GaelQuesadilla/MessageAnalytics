from typing import List, Dict, Union
import json
from src.models.Chat import Chat
from src.models.Message import Message
from pprint import pp
from pathlib import Path
from src.views.AllMessages import AllMessages
chat = Chat(file=None)


# file = Path.cwd() / "data" / "chats" / "CCO2.txt"
# chat.file = file
# chat.loadFromFile()

# file = Path.cwd() / "data" / "chats" / "IvannaSmp.txt"
# chat.file = file
# chat.loadFromFile()

# file = Path.cwd() / "data" / "chats" / "Ivanna.txt"
# chat.file = file
# chat.loadFromFile()

file = Path.cwd() / "data" / "chats" / "votouniv.txt"
chat.file = file
chat.loadFromFile()

pp(chat.stats())

print("\n\n\n")

auths: List[Dict[str, Union[str, int]]] = chat.stats().get("MessagesByAuthor")
pp(sorted(auths, key=lambda item: item.get("messages"), reverse=True))

# pp(chat.getWorldFrec().most_common(100))


# filePath = Path.cwd() / "data" / "data.json"
# data = chat.asJson()

# with filePath.open("w", encoding="UTF-8") as file:
#     file.write(data)


graph = AllMessages(chat)

graph.process()
graph.show()
