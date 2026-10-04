import tkinter as tk
from tkinter import messagebox
from app.config import BG,WHITE,NAVY,BLUE,MODEL_PARAMS,APP_VERSION,APP_DEPT,REPORTS_DIR,DB_PATH,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
class SettingsScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill='both',expand=True);Sidebar(self,controller,'settings');c=tk.Frame(self,bg=BG);c.pack(side='right',fill='both',expand=True);make_header(c,controller,'System Settings')
  card=tk.Frame(c,bg=WHITE);card.pack(fill='both',expand=True,padx=35,pady=30)
  acc='Not loaded'
  try:acc=f"{controller.load_predictor().get_accuracy()*100:.2f}%"
  except Exception:pass
  info=f"IDTEWS {APP_VERSION}\n\nDepartment: {APP_DEPT}\n\nMachine Learning Algorithm: CART Decision Tree\nModel Parameters: {MODEL_PARAMS}\nModel Accuracy: {acc}\n\nDatabase: {DB_PATH}\nReports Folder: {REPORTS_DIR}"
  tk.Label(card,text='System Information',bg=WHITE,fg=NAVY,font=("Times New Roman",18,'bold')).pack(anchor='w',padx=25,pady=20);tk.Label(card,text=info,bg=WHITE,fg=NAVY,font=FONT_NORMAL,justify='left').pack(anchor='w',padx=25)
  tk.Button(card,text='Check System Status',command=lambda:messagebox.showinfo('IDTEWS','System is operational. Database and model are available.'),bg=BLUE,fg=WHITE,font=FONT_NORMAL).pack(anchor='w',padx=25,pady=30)
