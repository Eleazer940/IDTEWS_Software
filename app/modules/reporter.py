import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from app.config import REPORTS_DIR,APP_FULL
class Reporter:
 @staticmethod
 def export_csv(df,path=None):
  os.makedirs(REPORTS_DIR,exist_ok=True);path=path or os.path.join(REPORTS_DIR,f"report_{datetime.now():%Y%m%d_%H%M%S}.csv");df.to_csv(path,index=False);return path
 @staticmethod
 def export_result_pdf(r,path=None):
  os.makedirs(REPORTS_DIR,exist_ok=True);path=path or os.path.join(REPORTS_DIR,f"prediction_{datetime.now():%Y%m%d_%H%M%S}.pdf");s=getSampleStyleSheet();rows=[["Field","Value"]]+[[k,str(v)] for k,v in r["features"].items()]+[["Prediction",r["predicted_class"]],["Confidence",f'{r["confidence"]:.2f}%']];SimpleDocTemplate(path,pagesize=A4).build([Paragraph(APP_FULL,s["Title"]),Spacer(1,15),Table(rows)]);return path
