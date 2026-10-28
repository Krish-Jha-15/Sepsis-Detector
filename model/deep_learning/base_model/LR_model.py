from model.deep_learning.base_model.train_test_split import X_train, X_test, y_train, y_test

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    confusion_matrix,
    classification_report
)

# -------------------------------
# Build Pipeline
# -------------------------------

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    ))
])

pipeline.fit(X_train, y_train)

# -------------------------------
# Predict probabilities
# -------------------------------

y_prob = pipeline.predict_proba(X_test)[:, 1]

# -------------------------------
# Threshold Selection
# -------------------------------

def best_threshold(y_true, y_prob, target_recall=0.80):

    precision, recall, thresholds = precision_recall_curve(
        y_true,
        y_prob
    )

    valid = np.where(recall[:-1] >= target_recall)[0]

    if len(valid) == 0:
        print("No threshold satisfies the target recall.")
        return 0.5

    best = valid[-1]

    print("=" * 40)
    print("Chosen Threshold :", round(thresholds[best], 4))
    print("Precision        :", round(precision[best], 4))
    print("Recall           :", round(recall[best], 4))
    print("=" * 40)

    return thresholds[best]


threshold = best_threshold(y_test, y_prob)

# -------------------------------
# Final Predictions
# -------------------------------

y_pred = (y_prob >= threshold).astype(int)

# -------------------------------
# Metrics
# -------------------------------

roc_auc = roc_auc_score(y_test, y_prob)
auprc = average_precision_score(y_test, y_prob)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\nModel Performance")
print("-" * 40)
print(f"ROC-AUC    : {roc_auc:.4f}")
print(f"AUPRC      : {auprc:.4f}")
print(f"Accuracy   : {accuracy:.4f}")
print(f"Precision  : {precision:.4f}")
print(f"Recall     : {recall:.4f}")
print(f"F1-Score   : {f1:.4f}")

print("\nPositive prevalence:", y_test.mean())

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))