# extensions file

from diddiparser.parser import def_func

_NAME = "Unknown"


def ask(s: str) -> None:
    "ask for a name and save it."
    _NAME = input(s)


def response(s: str) -> None:
    "use the name on your string 's'."
    try:
        print(s % _NAME)
    except Exception as e:
        print(f"ERROR: Could not print response: {str(e)}")


def_func("ask_for_name", ask)
def_func("say_with_name", response)
