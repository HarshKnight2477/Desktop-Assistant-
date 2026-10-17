"""Measure the intent classifier and write reports/evaluation.md.

Usage: python -m assistant.evaluate

Two measurements:
  * 5-fold stratified cross-validation on the training patterns
  * accuracy on held-out phrases (data/test_phrases.json) the model never saw
"""

import statistics
import time
from datetime import date

from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from assistant import config
from assistant.data_loader import load_intents, load_test_phrases
from assistant.nlp import IntentClassifier
from assistant.nlp.classifier import build_pipeline

LATENCY_ROUNDS = 20


def evaluate() -> dict:
    dataset = load_intents()
    texts, labels = dataset.training_data()

    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_predicted = cross_val_predict(build_pipeline(), texts, labels, cv=folds)

    classifier = IntentClassifier().fit(texts, labels)
    test_phrases = load_test_phrases()
    test_texts = [text for text, _ in test_phrases]
    test_labels = [tag for _, tag in test_phrases]
    test_predicted = [classifier.predict(text).intent for text in test_texts]

    timings = []
    for _ in range(LATENCY_ROUNDS):
        for text in test_texts:
            start = time.perf_counter()
            classifier.predict(text)
            timings.append((time.perf_counter() - start) * 1000)
    timings.sort()

    return {
        "intents": len(dataset.intents),
        "training_samples": len(texts),
        "test_samples": len(test_texts),
        "cv_accuracy": accuracy_score(labels, cv_predicted),
        "cv_macro_f1": f1_score(labels, cv_predicted, average="macro"),
        "test_accuracy": accuracy_score(test_labels, test_predicted),
        "test_macro_f1": f1_score(test_labels, test_predicted, average="macro"),
        "latency_mean_ms": statistics.mean(timings),
        "latency_p95_ms": timings[int(len(timings) * 0.95) - 1],
        "report": classification_report(test_labels, test_predicted, zero_division=0),
        "errors": [(t, want, got) for t, want, got in zip(test_texts, test_labels, test_predicted)
                   if want != got],
    }


def write_report(results: dict) -> str:
    errors = "\n".join(f"| {text} | {want} | {got} |" for text, want, got in results["errors"])
    report = f"""# Intent classifier evaluation

Generated on {date.today():%Y-%m-%d} by `python -m assistant.evaluate`.

| Metric | Value |
|---|---|
| Intents | {results['intents']} |
| Training samples | {results['training_samples']} |
| Held-out test phrases | {results['test_samples']} |
| 5-fold cross-validation accuracy | {results['cv_accuracy']:.1%} |
| 5-fold cross-validation macro F1 | {results['cv_macro_f1']:.3f} |
| Held-out test accuracy | {results['test_accuracy']:.1%} |
| Held-out test macro F1 | {results['test_macro_f1']:.3f} |
| Mean classification latency | {results['latency_mean_ms']:.2f} ms |
| p95 classification latency | {results['latency_p95_ms']:.2f} ms |

## Per-intent results (held-out phrases)

```
{results['report']}
```

## Misclassified held-out phrases

| Phrase | Expected | Predicted |
|---|---|---|
{errors or "| (none) | | |"}
"""
    config.REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.REPORT_PATH.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    results = evaluate()
    write_report(results)
    print(f"Intents: {results['intents']}   training samples: {results['training_samples']}   "
          f"held-out phrases: {results['test_samples']}")
    print(f"Cross-validation accuracy: {results['cv_accuracy']:.1%}  (macro F1 {results['cv_macro_f1']:.3f})")
    print(f"Held-out accuracy:         {results['test_accuracy']:.1%}  (macro F1 {results['test_macro_f1']:.3f})")
    print(f"Latency: mean {results['latency_mean_ms']:.2f} ms, p95 {results['latency_p95_ms']:.2f} ms")
    for text, want, got in results["errors"]:
        print(f"  miss: {text!r} expected {want}, got {got}")
    print(f"Report written to {config.REPORT_PATH.relative_to(config.PROJECT_DIR)}")


if __name__ == "__main__":
    main()
