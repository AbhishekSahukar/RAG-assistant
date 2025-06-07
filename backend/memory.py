
chat_memory = []

def add_message(user_msg, bot_msg):
    chat_memory.append({
        "user": user_msg,
        "assistant": bot_msg
    })

def clear():
    chat_memory.clear()

def get():
    return chat_memory
