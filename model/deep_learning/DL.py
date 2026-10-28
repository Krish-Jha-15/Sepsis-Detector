import sys
import os

import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score,roc_auc_score
import torch 
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
from torch.nn.utils.rnn import pad_sequence


project_root=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(project_root)

from model.deep_learning.base_model.train_test_split import train_data,test_data

save_dir = os.path.join(project_root, "saved_models")

os.makedirs(save_dir, exist_ok=True)


train_patient_outcomes=train_data.groupby('Patient_id')['SepsisLabel'].max().reset_index()
print('Patient_outcome')
print(train_patient_outcomes.head())

train_patient,val_patient=train_test_split(train_patient_outcomes,test_size=0.2,random_state=42,stratify=train_patient_outcomes['SepsisLabel'])

train_idx=train_patient['Patient_id']
val_idx=val_patient['Patient_id']

print("valuation Patient:",len(val_idx))
print("trainning Patient:",len(train_idx))

deep_train_data=train_data[train_data['Patient_id'].isin(train_idx)].copy()
deep_val_data=train_data[train_data['Patient_id'].isin(val_idx)].copy()

print("deep_train_data")
print(deep_train_data.head())

overlap=set(deep_train_data["Patient_id"])&set(deep_val_data['Patient_id'])
print("Patient overlap between train/val (should be empty):", overlap)

if(len(overlap) == 0):
    drop_columns=['Patient_id','SepsisLabel','dataset']
    feature_columns=[col for col in deep_train_data.columns if col not in drop_columns]

    print("Number of features:", len(feature_columns))


    Scale=StandardScaler()

    Scale.fit(deep_train_data[feature_columns])
    
    joblib.dump(
    feature_columns,
    os.path.join(save_dir, "feature_columns.pkl")
    )

    joblib.dump(
        Scale,
        os.path.join(save_dir, "scaler.pkl")
    )

    

    deep_train_data[feature_columns]=Scale.transform(deep_train_data[feature_columns])
    deep_val_data[feature_columns]=Scale.transform(deep_val_data[feature_columns])
    test_data[feature_columns]=Scale.transform(test_data[feature_columns])
    

    class SepsisSequenceDataSet(Dataset):

        def __init__(self,data,feature_col):
            self.sequence=[]

            data=data.sort_values(['Patient_id','ICULOS'])

            for Patient_id,Patient in data.groupby('Patient_id'):

                X = torch.tensor(Patient[feature_col].values, dtype=torch.float32)
                y=torch.tensor(Patient['SepsisLabel'].values, dtype=torch.float32)
                self.sequence.append((X,y))

        def __len__(self):
            return len(self.sequence)

        def __getitem__(self, index):
            return self.sequence[index]

    train_dataset=SepsisSequenceDataSet(deep_train_data,feature_columns)
    val_dataset=SepsisSequenceDataSet(deep_val_data,feature_columns)
    test_dataset=SepsisSequenceDataSet(test_data,feature_columns)

    print("Training patients After DataSet:", len(train_dataset))

    X,y=train_dataset[0]
    print('first patient X: ',X.shape)
    print('first patient y: ',y.shape)

    def collate_patient_sequence(batch):
        X_sequence=[item[0] for item in batch]
        Y_sequence=[item[1] for item in batch]

        length=torch.tensor([len(sequence) for sequence in X_sequence])

        X_padded=pad_sequence(X_sequence,batch_first=True,padding_value=0.0)
        y_padded=pad_sequence(Y_sequence,batch_first=True,padding_value=-1)

        return X_padded,y_padded,length
    
    train_loader=DataLoader(
        train_dataset,batch_size=32,shuffle=True,collate_fn=collate_patient_sequence
    )

    val_loader=DataLoader(
        val_dataset,batch_size=32,shuffle=False,collate_fn=collate_patient_sequence
    )

    test_loader=DataLoader(
        test_dataset,batch_size=32,shuffle=False,collate_fn=collate_patient_sequence
    )

    
    X_batch, y_batch, lengths = next(iter(train_loader))
    print("X:", X_batch.shape)
    print("y:", y_batch.shape)
    print("Lengths:", lengths)

    class SepsisGRU(nn.Module):

        def __init__(self,input_size,hidden_state,num_layer,dropout=0.0):
            super().__init__()

            self.GRU = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_state,
            num_layers=num_layer,
            dropout=dropout if num_layer > 1 else 0,
            batch_first=True
        )

            self.output=nn.Linear(hidden_state,1)

        def forward(self,x):

            gru_output,_=self.GRU(x)
            logists=self.output(gru_output).squeeze(-1)
            return logists
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print('Device',device)

    if device.type =='cuda':

        model=SepsisGRU(
            input_size=len(feature_columns),
            hidden_state=64,
            num_layer=1
        ).to(device)
        
        neg=(deep_train_data['SepsisLabel']==0).sum()
        pos=(deep_train_data['SepsisLabel']==1).sum()
        pos_weight=torch.tensor(
            [neg/max(pos,1)],
            dtype=torch.float32,
            device=device
        )

        print("pos_weight:", pos_weight)

        cerition=nn.BCEWithLogitsLoss(pos_weight=pos_weight)

        optimizer=torch.optim.Adam(
            model.parameters(),
            lr=0.001
        )

        best_auprc=0
        model_path = os.path.join(save_dir, "dl_best_model.pth")
        def evaluate_model(model,val_loader,device):
            model.eval()

            all_probabilities = []
            all_labels = []
            with torch.no_grad():

                for X_batch,y_batch,length in val_loader:

                    X_batch=X_batch.to(device)
                    y_batch=y_batch.to(device)

                    logits = model(X_batch)
                    probabilities = torch.sigmoid(logits)

                    mask = y_batch != -1  

                    all_probabilities.extend(probabilities[mask].detach().cpu().numpy())
                    all_labels.extend(y_batch[mask].detach().cpu().numpy())


                auprc = average_precision_score(all_labels, all_probabilities)
                roc_auc = roc_auc_score(all_labels, all_probabilities)

                return auprc,roc_auc

        epochs=10

        for epoch in range(epochs):

            model.train()
            total_loss=0

            for X_batch,y_batch,lengths in train_loader:

                X_batch=X_batch.to(device)
                y_batch=y_batch.to(device)

                optimizer.zero_grad()

                logists=model(X_batch)
                mask=y_batch != -1
                loss=cerition(logists[mask],y_batch[mask])
                loss.backward()

                torch.nn.utils.clip_grad_norm_(model.parameters(),max_norm=0.1)

                optimizer.step()
                total_loss+=loss.item()
            average_loss=total_loss/len(train_loader)

            auprc,roc_auc=evaluate_model(model,val_loader,device)
            
            print(
                    f"Epoch {epoch + 1} | "
                    f"Train Loss: {average_loss:.4f} | "
                    f"Val AUPRC: {auprc:.4f} | "
                    f"Val ROC-AUC: {roc_auc:.4f}"
                )

            if auprc>best_auprc:
                    best_auprc=auprc
                    torch.save(model.state_dict(),model_path)
                    print(f"  -> New best model saved (AUPRC: {best_auprc:.4f})")
        
        model.load_state_dict(torch.load(model_path, map_location=device))

        test_auprc, test_roc = evaluate_model(model, test_loader, device)
        print(f"Test AUPRC: {test_auprc:.4f} | Test ROC-AUC: {test_roc:.4f}")

    else:
        print('GPU Is Not connected')    

else:
    print("Overlap Should be Empty ||||| []")