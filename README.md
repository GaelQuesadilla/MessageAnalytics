# Message Analytics

## Parser

### Patterns

- datetime : r"\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}\s?[a.p.]?.\s?m."
- content : r"(?<=: )(.\*)"
- author : r"(?<= - )(.\*)(?=:)"
