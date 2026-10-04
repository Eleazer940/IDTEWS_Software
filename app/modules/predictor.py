import pandas as pd,numpy as np
from app.modules.trainer import ModelTrainer
from app.config import FEATURES
class Predictor:
 def __init__(self):
  p=ModelTrainer.load();self.model=p["model"];self.scaler=p["scaler"];self.le=p["le"];self.features=p["features"];self.metrics=p.get("metrics",{})
 def score(self,d):return .25*d["attendance_pct"]+.25*d["assignment_score"]+.30*d["midterm_score"]+.10*d["participation"]*10+.10*d["previous_gpa"]*25
 def predict_single(self,d):
  X=pd.DataFrame([[float(d[x]) for x in self.features]],columns=self.features);z=self.scaler.transform(X);i=int(self.model.predict(z)[0]);pr=self.model.predict_proba(z)[0];labs=self.le.inverse_transform(self.model.classes_);return {"predicted_class":self.le.inverse_transform([i])[0],"confidence":float(pr.max()*100),"probabilities":{str(labs[j]):float(pr[j]*100) for j in range(len(labs))},"weighted_score":float(self.score(d)),"feature_importance":self.get_feature_importance(),"features":{x:float(d[x]) for x in self.features}}
 def predict_batch(self,df):
  df=df.copy();X=df[self.features].astype(float);z=self.scaler.transform(X);df["predicted_class"]=self.le.inverse_transform(self.model.predict(z));df["confidence"]=self.model.predict_proba(z).max(axis=1)*100;df["weighted_score"]=X.apply(self.score,axis=1);return df
 def get_feature_importance(self):return {x:float(v) for x,v in zip(self.features,self.model.feature_importances_)}
 def get_accuracy(self):return float(self.metrics.get("accuracy",0))
 def get_metrics(self):return self.metrics
