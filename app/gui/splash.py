import tkinter as tk
from app.config import NAVY, BLUE, WHITE, APP_FULL, APP_VERSION

class SplashScreen(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.overrideredirect(True)
        self.configure(bg=NAVY)
        w,h=560,310
        x=(self.winfo_screenwidth()-w)//2; y=(self.winfo_screenheight()-h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")
        tk.Label(self,text="IDTEWS",bg=NAVY,fg=WHITE,font=("Times New Roman",30,"bold")).pack(pady=(55,5))
        tk.Label(self,text="INTELLIGENT ACADEMIC EARLY WARNING SYSTEM",bg=NAVY,fg="#DDE7F5",font=("Times New Roman",11,"bold")).pack()
        tk.Label(self,text="Decision Tree • Explainable Predictions • Early Intervention",bg=NAVY,fg="#BFCDE0",font=("Times New Roman",10)).pack(pady=15)
        bar=tk.Frame(self,bg=BLUE,width=420,height=10); bar.pack(pady=20); bar.pack_propagate(False)
        tk.Label(self,text=f"Loading {APP_VERSION}",bg=NAVY,fg=WHITE,font=("Times New Roman",10)).pack()
