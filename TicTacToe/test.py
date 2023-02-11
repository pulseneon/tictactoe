from language.langs import Language

langs = Language()
def get_string(string: str) -> str:
    return langs.get_string(string)

print(get_string("curr_chat_lansg"))
print(get_string("curr_chat_lang"))
#print(langs.get_languages())