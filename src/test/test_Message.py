import unittest
from datetime import datetime
from src.models.Message import Message


class TestMessageMethods(unittest.TestCase):

    def setUp(self):
        self.message_raw = "10/5/2024, 11:24 p. m. - Gael: Los datos que tengo disponibles son: NO. LISTA	NOMBRE	GRADO	GRUPO	TURNO	PAQUETE	TUTOR	FOTO	FRASE\n"
        self.message = Message(raw=self.message_raw)

    def test_getDate(self):
        date_pattern = r"\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}\s?[a.p.]?.\s?m."
        date_format = "%d/%m/%Y, %I:%M %p"

        self.message.getDate(date_pattern, date_format)

        expected_date = datetime(2024, 5, 10, 23, 24)
        self.assertEqual(self.message.date, expected_date)

    def test_getAuthor(self):
        author_pattern = r"(?<= - )(.*)(?=:)"
        self.message.getAuthor(author_pattern)

        self.assertEqual(self.message.author, "Gael")

    def test_getContent(self):
        content_pattern = r"(?<=: )(.*)"

        self.message.getContent(content_pattern)

        self.assertEqual(
            self.message.content, "Los datos que tengo disponibles son: NO. LISTA	NOMBRE	GRADO	GRUPO	TURNO	PAQUETE	TUTOR	FOTO	FRASE\n")


if __name__ == "__main__":
    unittest.main()
