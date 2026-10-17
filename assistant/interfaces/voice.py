"""Voice chat: speech recognition in, text-to-speech out.

Needs the optional extras: pip install -r requirements-voice.txt
"""

from assistant import config
from assistant.chatbot import Chatbot
from assistant.interfaces.cli import format_reply


class VoiceUnavailable(RuntimeError):
    pass


def run(bot: Chatbot, debug: bool = False) -> None:
    try:
        import pyttsx3
        import speech_recognition as sr
    except ImportError:
        raise VoiceUnavailable(
            "Voice mode needs extra packages. Install them with: pip install -r requirements-voice.txt"
        )

    engine = pyttsx3.init()
    recognizer = sr.Recognizer()

    def say(text: str) -> None:
        engine.say(text)
        engine.runAndWait()

    print(f"{config.ASSISTANT_NAME}: Listening. Say \"bye\" to stop (Ctrl+C to force quit).")
    say("Hi, I'm listening.")
    with sr.Microphone() as microphone:
        recognizer.adjust_for_ambient_noise(microphone, duration=0.5)
        while True:
            try:
                audio = recognizer.listen(microphone, timeout=8, phrase_time_limit=8)
                message = recognizer.recognize_google(audio)
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except sr.RequestError:
                print("Speech service unreachable; check your internet connection.")
                continue
            except KeyboardInterrupt:
                break

            print(f"You: {message}")
            reply = bot.reply(message)
            print(format_reply(reply, debug))
            say(reply.text)
            if reply.ends_conversation:
                break
