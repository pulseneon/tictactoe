import os
import yaml

class Language:
    def __init__(self) -> None:
        self.languages: dict = {}
        self.update_languages()

    def get_string(self, string: str):
        lang = self.get_language()
        try:
            if lang in self.get_languages():
                return self.languages[lang][string]
            else:
                raise NotAvailable
        except KeyError:
            # en.yaml should always be available
            return self.get_default_string(string)
        except NotAvailable:
            # changing the language to basic and return his
            return self.get_default_string(string)

    def get_string_by_lang(self, string: str, lang: str) -> str:
        try:
            return self.languages[lang][string]
        except KeyError:
            return self.get_default_string(string)

    def get_default_string(self, string: str):
        en_string = self.languages['en'].get(string)
        if en_string is None:
            return StringNotFound(f'Error: string "{string}" not found.')
        return en_string

    # reload available langs
    def update_languages(self):
        path = r'./TicTacToe/language/' # /TicTacToe
        for filename in os.listdir(path):
            if filename.endswith('.yaml'):
                language_name = filename[:-5]
                self.languages[language_name] = yaml.safe_load(
                    open(path + filename, encoding='utf8')
                )

    def get_language(self):
        # import lang from db and return then
        # for test return en
        return 'en'

    # for generate keyboard
    def get_languages(self) -> list:
        to_return = []
        for lang in self.languages:
            if self.languages[lang]['available']:
                to_return.append(lang)
        return to_return

    def get_languages_names(self) -> list:
        to_return = []
        for lang in self.languages:
            if self.languages[lang]['available']:
                to_return.append(self.languages[lang]['language'])
        return to_return

languages = Language()


def return_error_str(string):
    return string


class StringNotFound(Exception):
    """
    if ru.yaml also gives an error and there is no localization at all
    """
    def __init__(self, *args: object) -> None:
        return_error_str(''.join(args))


class NotAvailable(Exception):
    """
    if the user's language is not currently available
    """

    def __init__(self, *args: object) -> None:
        # !need to change user lang to ru!
        user_lang = 'en'