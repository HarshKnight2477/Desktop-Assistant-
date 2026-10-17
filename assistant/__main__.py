"""Entry point.  Usage: python -m assistant [--voice] [--debug]"""

import argparse

from assistant.chatbot import Chatbot


def main() -> None:
    parser = argparse.ArgumentParser(prog="assistant", description="NLP desktop assistant")
    parser.add_argument("--voice", action="store_true", help="talk instead of type")
    parser.add_argument("--debug", action="store_true", help="show intent, confidence and latency")
    args = parser.parse_args()

    bot = Chatbot.from_disk()
    if args.voice:
        from assistant.interfaces import voice
        try:
            voice.run(bot, debug=args.debug)
        except voice.VoiceUnavailable as error:
            parser.exit(1, f"{error}\n")
    else:
        from assistant.interfaces import cli
        cli.run(bot, debug=args.debug)


if __name__ == "__main__":
    main()
