"""Train the intent classifier and save it.  Usage: python -m assistant.train"""

from assistant import config
from assistant.data_loader import IntentDataset, load_intents
from assistant.nlp import IntentClassifier


def train(dataset: IntentDataset | None = None) -> IntentClassifier:
    dataset = dataset or load_intents()
    texts, labels = dataset.training_data()
    classifier = IntentClassifier().fit(texts, labels)
    classifier.save(config.MODEL_PATH)
    return classifier


def main() -> None:
    dataset = load_intents()
    texts, _ = dataset.training_data()
    train(dataset)
    print(f"Trained on {len(texts)} samples across {len(dataset.intents)} intents.")
    print(f"Model saved to {config.MODEL_PATH.relative_to(config.PROJECT_DIR)}")


if __name__ == "__main__":
    main()
