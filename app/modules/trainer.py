import os,pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from app.config import MODEL_PARAMS,MODEL_PATH,FEATURES
class ModelTrainer:
 def __init__(self):self.model=DecisionTreeClassifier(**MODEL_PARAMS);self.metrics={}
 def train(self,X,y):self.model.fit(X,y);return self.model
 def evaluate(self,X,y,class_names):
  p=self.model.predict(X);self.metrics={"accuracy":float(accuracy_score(y,p)),"classification_report":classification_report(y,p,target_names=list(class_names),zero_division=0),"confusion_matrix":confusion_matrix(y,p).tolist()};return self.metrics
 def save(self,scaler,le):
  os.makedirs(os.path.dirname(MODEL_PATH),exist_ok=True)
  with open(MODEL_PATH,"wb") as f:pickle.dump({"model":self.model,"scaler":scaler,"le":le,"features":FEATURES,"metrics":self.metrics},f)
 @staticmethod
 def load():
  with open(MODEL_PATH,"rb") as f:return pickle.load(f)
