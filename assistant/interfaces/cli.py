"""Text chat in the terminal."""

from assistant import config
from assistant.chatbot import Chatbot, Reply


def format_reply(reply: Reply, debug: bool) -> str:
    text = f"{config.ASSISTANT_NAME}: {reply.text}"
    if debug:
        text += f"\n  [intent={reply.intent} confidence={reply.confidence:.2f} {reply.latency_ms:.1f} ms]"
    return text


def run(bot: Chatbot, debug: bool = False) -> None:
    print(f"{config.ASSISTANT_NAME}: Hi! Type a message, \"help\" for ideas, or \"bye\" to quit.")
    while True:
        try:
            message = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        reply = bot.reply(message)
        print(format_reply(reply, debug))
        if reply.ends_conversation:
            break
