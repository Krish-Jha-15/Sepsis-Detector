from model.deep_learning.base_model.train_test_split import X_train,X_test,y_train,y_test 

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

# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestClassifier
# param_grid = {
#     "n_estimators": [100,200,300,400],
#     "criterion": ["gini","entropy","log_loss"],
#     "max_depth": [2,4,5,6,8,10],
#     "min_samples_leaf": [1,3,5,7,9]
# }

# rf = RandomForestClassifier(
#     class_weight="balanced",
#     random_state=42,
#     n_jobs=1
# )

# grid = GridSearchCV(
#     rf,
#     param_grid,
#     scoring="average_precision",
#     cv=4,
#     n_jobs=-1,
#     verbose=2
# )

# grid.fit(X_train, y_train)

# print(grid.best_params_)
# print(grid.best_score_)



from sklearn.ensemble import RandomForestClassifier

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=5,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42
)

random_forest_model.fit(
    X_train,
    y_train
)


rf_prob = random_forest_model.predict_proba(
    X_test
)[:, 1]


rf_roc_auc = roc_auc_score(
    y_test,
    rf_prob
)

rf_auprc = average_precision_score(
    y_test,
    rf_prob
)

print("Random Forest ROC-AUC:", rf_roc_auc)
print("Random Forest AUPRC:", rf_auprc)