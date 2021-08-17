# extensions file

from diddiparser.parser import def_func


def ask(s: str) -> None:
    "ask for a name and save it."
    name = input(s)
    print(f"Hello, {name}. I am DiddiScript.")


def_func("ask_for_name", ask_and_response)
