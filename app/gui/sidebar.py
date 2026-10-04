import tkinter as tk
from app.config import SIDEBAR, BLUE, NAVY, WHITE, FONT_NORMAL, FONT_BOLD

class Sidebar(tk.Frame):
    def __init__(self, parent, controller, active=""):
        super().__init__(parent, bg=SIDEBAR, width=190)
        self.pack(side="left", fill="y")
        self.pack_propagate(False)
        tk.Label(self,text="IDTEWS",bg=SIDEBAR,fg=WHITE,font=("Times New Roman",18,"bold")).pack(anchor="w",padx=18,pady=(22,2))
        tk.Label(self,text="EARLY WARNING SYSTEM",bg=SIDEBAR,fg="#BDC3C7",font=("Times New Roman",8,"bold")).pack(anchor="w",padx=18,pady=(0,18))
        items=[
            ("dashboard","Dashboard",controller.show_dashboard),
            ("data","New Prediction",controller.show_data_entry),
            ("upload","CSV Upload",controller.show_csv_upload),
            ("history","Prediction History",controller.show_history),
            ("search","Student Search",controller.show_search),
            ("profile","Student Profile",controller.show_profile),
            ("alerts","Early Warning Alerts",controller.show_alerts),
            ("users","User Management",controller.show_users),
            ("settings","System Settings",controller.show_settings),
        ]
        for key,label,cmd in items:
            if key in ("users","settings") and (controller.current_user or {}).get("role") != "admin":
                continue
            b=tk.Button(self,text=label,command=cmd,bg=BLUE if key==active else SIDEBAR,fg=WHITE,relief="flat",bd=0,font=FONT_NORMAL,anchor="w",padx=18,activebackground=BLUE,activeforeground=WHITE)
            b.pack(fill="x",pady=1,ipady=8)
        tk.Frame(self,bg=SIDEBAR).pack(fill="both",expand=True)
        tk.Button(self,text="Logout",command=controller.logout,bg=NAVY,fg=WHITE,relief="flat",font=FONT_BOLD,pady=9).pack(fill="x",padx=12,pady=14)
