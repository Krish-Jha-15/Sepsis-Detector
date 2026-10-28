import pandas as pd
from model.deep_learning.base_model.LR_model import (roc_auc as logistic_roc_auc,auprc as logistic_auprc)
from model.deep_learning.base_model.RF_model import (rf_auprc,rf_roc_auc)
from model.deep_learning.base_model.XG_model import (xgb_auprc,xgb_roc_auc)

results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest",
        "XGBoost"
    ],
    "ROC_AUC": [
        logistic_roc_auc,
        rf_roc_auc,
        xgb_roc_auc
    ],
    "AUPRC": [
        logistic_auprc,
        rf_auprc,
        xgb_auprc
    ]
})

results = results.sort_values(
    "AUPRC",
    ascending=False
)

print(results)