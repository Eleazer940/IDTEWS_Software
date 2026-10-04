import os,sys
BASE_DIR=os.path.abspath(os.path.dirname(__file__));sys.path.insert(0,BASE_DIR)
def main():
 print("IDTEWS — One-Time Setup")
 for x in ["data","model","reports"]:os.makedirs(os.path.join(BASE_DIR,x),exist_ok=True)
 try:
  from app.database import init_db;init_db();print("Database initialised")
  from data.generate_dataset import generate_dataset;df=generate_dataset(os.path.join(BASE_DIR,"data","idtews_dataset.csv"));print("Dataset generated: 600 records")
  from app.modules.preprocessor import Preprocessor
  from app.modules.trainer import ModelTrainer
  pre=Preprocessor();Xtr,Xte,ytr,yte,dfp,_=pre.run_pipeline(df);t=ModelTrainer();t.train(Xtr,ytr);m=t.evaluate(Xte,yte,pre.le.classes_);t.save(pre.scaler,pre.le);print(f"Accuracy: {m['accuracy']*100:.2f}%");print(dfp.performance_category.value_counts());print("Setup complete! Run: python main.py")
 except ImportError as e:print("Missing package:",e,"\nRun: pip install -r requirements.txt");return 1
 return 0
if __name__=="__main__":raise SystemExit(main())
