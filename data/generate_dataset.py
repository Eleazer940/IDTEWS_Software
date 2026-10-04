import os,numpy as np,pandas as pd
def generate_dataset(output_path=None):
 np.random.seed(42);rows=[];groups=[(180,51,12,47,13,43,13,(1,4),1,.52),(270,72,10,68,10,65,11,(4,8),2.2,.55),(150,88,7,85,8,83,8,(7,10),3.45,.38)]
 for n,a,sa,b,sb,c,sc,p,g,sg in groups:
  for _ in range(n):rows.append([np.clip(np.random.normal(a,sa),30,100),np.clip(np.random.normal(b,sb),20,100),np.clip(np.random.normal(c,sc),20,100),np.random.uniform(*p),np.clip(np.random.normal(g,sg),0,4)])
 df=pd.DataFrame(rows,columns=["attendance_pct","assignment_score","midterm_score","participation","previous_gpa"]).sample(frac=1,random_state=42).reset_index(drop=True)
 df["weighted_score"]=.25*df.attendance_pct+.25*df.assignment_score+.30*df.midterm_score+.10*df.participation*10+.10*df.previous_gpa*25
 df["performance_category"]=np.where(df.weighted_score<57,"At-Risk",np.where(df.weighted_score<74,"Average","High-Achiever"));df=df.round(2)
 if output_path is None:output_path=os.path.join(os.path.dirname(__file__),"idtews_dataset.csv")
 df.to_csv(output_path,index=False);print("Dataset generated:",len(df),"records");print(df.performance_category.value_counts());return df
if __name__=="__main__":generate_dataset()
