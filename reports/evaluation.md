# Intent classifier evaluation

Generated on 2026-10-17 by `python -m assistant.evaluate`.

| Metric | Value |
|---|---|
| Intents | 15 |
| Training samples | 337 |
| Held-out test phrases | 60 |
| 5-fold cross-validation accuracy | 79.8% |
| 5-fold cross-validation macro F1 | 0.797 |
| Held-out test accuracy | 93.3% |
| Held-out test macro F1 | 0.933 |
| Mean classification latency | 0.79 ms |
| p95 classification latency | 0.87 ms |

## Per-intent results (held-out phrases)

```
              precision    recall  f1-score   support

capabilities       0.80      1.00      0.89         4
   close_app       1.00      1.00      1.00         4
        date       1.00      1.00      1.00         4
     goodbye       0.80      1.00      0.89         4
    greeting       1.00      0.75      0.86         4
    identity       1.00      0.75      0.86         4
        joke       1.00      1.00      1.00         4
    open_app       1.00      1.00      1.00         4
 open_folder       1.00      1.00      1.00         4
open_website       1.00      1.00      1.00         4
      thanks       1.00      1.00      1.00         4
        time       1.00      1.00      1.00         4
     weather       0.80      1.00      0.89         4
  web_search       1.00      0.75      0.86         4
   wellbeing       0.75      0.75      0.75         4

    accuracy                           0.93        60
   macro avg       0.94      0.93      0.93        60
weighted avg       0.94      0.93      0.93        60

```

## Misclassified held-out phrases

| Phrase | Expected | Predicted |
|---|---|---|
| hey assistant | greeting | goodbye |
| are you an ai | identity | wellbeing |
| you doing okay? | wellbeing | capabilities |
| google the weather of mars | web_search | weather |
