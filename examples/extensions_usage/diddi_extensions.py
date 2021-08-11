# extensions file

from diddiparser.parser import def_func

NAME = "Unknown"

def ask(s: str) -> None:
    "ask for a name and save it."
    NAME = input(s)

def response(s: str) -> None:
    "use the name on your string 's'."
    try:
        print(s%NAME)
    except:
        print(s)

def_func("ask_for_name", ask)
def_func("say_with_name", response)
