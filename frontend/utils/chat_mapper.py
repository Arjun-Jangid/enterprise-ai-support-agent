from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def build_langchain_history(messages):
    chat_history = []
    chat_history.append(SystemMessage(content="You are a helpful document Question/Answer assistant, that gives short answers."))

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")

        if role == "user":
            chat_history.append(HumanMessage(content=content))
        
        elif role == "assistant":
            chat_history.append(AIMessage(content=content))

    return chat_history