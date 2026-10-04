import tkinter as tk,matplotlib
from tkinter import messagebox
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.config import BG,WHITE,CAT_COLORS,NAVY,FONT_NORMAL,FONT_HEADING
from app.modules.recommender import Recommender
from app.modules.reporter import Reporter
class ResultScreen(tk.Frame):
 def __init__(self,parent,controller,r):
  super().__init__(parent,bg=BG);self.pack(fill="both",expand=True);self.r=r;make_header(self,controller,"Prediction Result");b=tk.Frame(self,bg=BG);b.pack(fill="both",expand=True);Sidebar(b,controller);c=tk.Frame(b,bg=BG,padx=20,pady=15);c.pack(side="left",fill="both",expand=True);cls=r["predicted_class"];tk.Label(c,text=f"Prediction: {cls} | Confidence: {r['confidence']:.2f}% | Weighted Score: {r['weighted_score']:.2f}",bg=CAT_COLORS[cls],fg=WHITE,font=FONT_HEADING,pady=12).pack(fill="x");p=tk.Frame(c,bg=BG);p.pack(fill="both",expand=True,pady=10);l=tk.Frame(p,bg=WHITE);l.pack(side="left",fill="both",expand=True);rr=tk.Frame(p,bg=WHITE);rr.pack(side="left",fill="both",expand=True,padx=8)
  f=Figure(figsize=(5,4));a=f.add_subplot(111);imp=r["feature_importance"];a.barh(list(imp),list(imp.values()));a.set_title("Feature Importance");f.tight_layout();can=FigureCanvasTkAgg(f,l);can.draw();can.get_tk_widget().pack(fill="both",expand=True)
  tk.Label(rr,text="Recommended Interventions",bg=WHITE,fg=NAVY,font=FONT_HEADING).pack(anchor="w",padx=15,pady=10)
  for x in Recommender.get_recommendations(cls):tk.Label(rr,text="• "+x,bg=WHITE,font=FONT_NORMAL,wraplength=350,justify="left").pack(anchor="w",padx=15,pady=2)
  tk.Label(rr,text=Recommender.explain(cls,r["features"],imp),bg=WHITE,font=FONT_NORMAL,wraplength=350,justify="left").pack(padx=15,pady=10)
  q=tk.Frame(c,bg=BG);q.pack();tk.Button(q,text="EXPORT PDF",command=lambda:self.pdf(),bg=NAVY,fg=WHITE,font=FONT_NORMAL).pack(side="left",padx=3);tk.Button(q,text="NEW PREDICTION",command=controller.show_data_entry,bg="#2C3E6B",fg=WHITE,font=FONT_NORMAL).pack(side="left",padx=3);tk.Button(q,text="DASHBOARD",command=controller.show_dashboard,bg="#3498DB",fg=WHITE,font=FONT_NORMAL).pack(side="left",padx=3)
 def pdf(self):
  try:messagebox.showinfo("Export",Reporter.export_result_pdf(self.r))
  except Exception as e:messagebox.showerror("Export Error",str(e))
