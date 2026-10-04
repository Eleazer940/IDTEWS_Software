import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,LabelEncoder
from app.config import FEATURES,THRESHOLD_AT_RISK,THRESHOLD_AVERAGE
class Preprocessor:
 def __init__(self):self.scaler=StandardScaler();self.le=LabelEncoder();self.log=[]
 def score(self,d):return .25*d["attendance_pct"]+.25*d["assignment_score"]+.30*d["midterm_score"]+.10*d["participation"]*10+.10*d["previous_gpa"]*25
 def run_pipeline(self,df,test_size=.30):
  df=df.copy();self.log=["1. Input validation"]
  if any(x not in df for x in FEATURES):raise ValueError("Missing required feature columns")
  df=df.dropna(subset=FEATURES)
  for x in FEATURES:df[x]=pd.to_numeric(df[x],errors="coerce")
  df=df.dropna(subset=FEATURES);self.log.append("2. Missing values and numeric conversion")
  df["weighted_score"]=df.apply(self.score,axis=1) if "weighted_score" not in df else df["weighted_score"]
  df["performance_category"]=df["weighted_score"].map(lambda x:"At-Risk" if x<57 else ("Average" if x<74 else "High-Achiever")) if "performance_category" not in df else df["performance_category"];self.log.append("3. Scoring and labelling")
  y=self.le.fit_transform(df["performance_category"]);X=df[FEATURES]
  a,b,c,d=train_test_split(X,y,test_size=test_size,random_state=42,stratify=y)
  self.log.append("4. Train/test split");return self.scaler.fit_transform(a),self.scaler.transform(b),c,d,df,self.log
 def transform_single(self,d):return self.scaler.transform(pd.DataFrame([[d[x] for x in FEATURES]],columns=FEATURES))
 def transform_batch(self,d):return self.scaler.transform(d[FEATURES])
 def decode_label(self,i):return self.le.inverse_transform([int(i)])[0]
 def get_log(self):return self.log
