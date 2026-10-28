from xgboost import XGBClassifier

from model.deep_learning.base_model.train_test_split import X_train,X_test,y_train,y_test 

from sklearn.metrics import roc_auc_score,average_precision_score

negative_count = (y_train == 0).sum()
positive_count = (y_train == 1).sum()

scale_pos_weight = (
    negative_count / positive_count
)

print("Negative:", negative_count)
print("Positive:", positive_count)
print("scale_pos_weight:", scale_pos_weight)

xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(
    X_train,
    y_train
)


xgb_prob = xgb_model.predict_proba(
    X_test
)[:, 1]


xgb_roc_auc = roc_auc_score(
    y_test,
    xgb_prob
)

xgb_auprc = average_precision_score(
    y_test,
    xgb_prob
)

print("XGBoost ROC-AUC:", xgb_roc_auc)
print("XGBoost AUPRC:", xgb_auprc)