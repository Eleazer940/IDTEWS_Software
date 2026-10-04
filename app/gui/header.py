import tkinter as tk
from app.config import NAVY,WHITE,FONT_HEADING,FONT_SMALL,APP_NAME
def make_header(parent,controller,title):
 b=tk.Frame(parent,bg=NAVY,height=55);b.pack(fill="x");b.pack_propagate(False);tk.Label(b,text=APP_NAME,bg=NAVY,fg=WHITE,font=FONT_HEADING).pack(side="left",padx=18);tk.Label(b,text="| "+title,bg=NAVY,fg=WHITE,font=("Times New Roman",12)).pack(side="left");tk.Label(b,text="User: "+(controller.current_user or {}).get("username",""),bg=NAVY,fg=WHITE,font=FONT_SMALL).pack(side="right",padx=15);return b
