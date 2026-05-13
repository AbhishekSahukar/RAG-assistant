from typing import List, Dict

_history: List[Dict[str, str]] = []


def add_message(user_msg: str, bot_msg: str) -> None:
    _history.append({"user": user_msg, "assistant": bot_msg})


def get_history() -> List[Dict[str, str]]:
    return _history


def clear_history() -> None:
    _history.clear()