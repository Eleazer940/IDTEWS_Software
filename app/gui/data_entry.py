import tkinter as tk
from tkinter import messagebox
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.config import BG,WHITE,NAVY,BLUE,FEATURES,FEATURE_LABELS,FEATURE_RANGES,FONT_NORMAL,FONT_HEADING
from app.database import save_prediction
class DataEntryScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill="both",expand=True);self.controller=controller;make_header(self,controller,"Student Data Entry");b=tk.Frame(self,bg=BG);b.pack(fill="both",expand=True);Sidebar(b,controller,"data");c=tk.Frame(b,bg=BG,padx=30,pady=25);c.pack(side="left",fill="both",expand=True);tk.Label(c,text="Enter Student Academic Information",bg=BG,fg=NAVY,font=FONT_HEADING).pack(anchor="w");card=tk.Frame(c,bg=WHITE,padx=25,pady=20);card.pack(fill="x",pady=15);self.e={}
  tk.Label(card,text="Student ID",bg=WHITE,font=FONT_NORMAL).grid(row=0,column=0,sticky="w",pady=6);self.sid=tk.Entry(card,font=FONT_NORMAL);self.sid.grid(row=0,column=1,pady=6)
  for i,x in enumerate(FEATURES,1):tk.Label(card,text=FEATURE_LABELS[x],bg=WHITE,font=FONT_NORMAL).grid(row=i,column=0,sticky="w",pady=6);self.e[x]=tk.Entry(card,font=FONT_NORMAL);self.e[x].grid(row=i,column=1,pady=6)
  tk.Button(c,text="PREDICT",command=self.go,bg=NAVY,fg=WHITE,font=FONT_NORMAL,width=14).pack(side="left",padx=3);tk.Button(c,text="CLEAR",command=self.clear,bg=BLUE,fg=WHITE,font=FONT_NORMAL,width=12).pack(side="left",padx=3);tk.Button(c,text="UPLOAD",command=controller.show_csv_upload,bg="#3498DB",fg=WHITE,font=FONT_NORMAL,width=12).pack(side="left",padx=3)
 def clear(self):
  self.sid.delete(0,"end")
  for e in self.e.values():e.delete(0,"end")
 def go(self):
  try:
   if not self.sid.get().strip():raise ValueError("Student ID is required.")
   d={x:float(self.e[x].get()) for x in FEATURES}
   for x,v in d.items():
    a,b=FEATURE_RANGES[x]
    if not a<=v<=b:raise ValueError(f"{FEATURE_LABELS[x]} must be between {a} and {b}.")
   r=self.controller.predictor.predict_single(d);r["student_id"]=self.sid.get().strip();save_prediction(r["student_id"],d,r["predicted_class"],r["confidence"]);self.controller.show_result(r)
  except Exception as e:messagebox.showerror("Validation/Prediction Error",str(e))
