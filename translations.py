locale = 'pl'

languages = {
    'en': {
        'points': 'Points:',
        'enter_level': 'Choose level (1-100)'
    },
    'pl': {
        'points': 'Punkty:',
        'enter_level': 'Wybierz poziom (1-100)'
    }
}


def translate(label: str) -> str:
    return str(languages[locale][label])
