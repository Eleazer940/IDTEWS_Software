import tkinter as tk
from app.config import APP_FULL
from app.gui.login import LoginScreen
from app.gui.data_entry import DataEntryScreen
from app.gui.result import ResultScreen
from app.gui.csv_upload import CsvUploadScreen
from app.gui.dashboard import DashboardScreen
from app.gui.history import HistoryScreen
from app.gui.search import SearchScreen
from app.gui.alerts import AlertsScreen
from app.gui.users import UsersScreen
from app.gui.settings import SettingsScreen
from app.gui.profile import StudentProfileScreen
from app.modules.predictor import Predictor
from app.gui.splash import SplashScreen

class MainWindow:
    def __init__(self):
        self.root=tk.Tk(); self.root.title(APP_FULL); self.root.geometry("1280x780"); self.root.minsize(1050,650)
        self.current_user=None; self.predictor=None; self.last_result=None; self.last_batch_df=None; self.screen=None
        self.root.withdraw(); self.root.protocol("WM_DELETE_WINDOW",self.root.destroy)
        splash=SplashScreen(self.root)
        self.root.after(1200, lambda: (splash.destroy(), self.root.deiconify(), self.show_login()))
    def run(self): self.root.mainloop()
    def show(self, cls,*args):
        if self.screen is not None:
            try:self.screen.destroy()
            except tk.TclError:pass
        self.screen=cls(self.root,self,*args)
    def show_login(self): self.show(LoginScreen)
    def show_data_entry(self): self.show(DataEntryScreen)
    def show_result(self,result): self.last_result=result; self.show(ResultScreen,result)
    def show_csv_upload(self): self.show(CsvUploadScreen)
    def show_dashboard(self): self.show(DashboardScreen)
    def show_history(self): self.show(HistoryScreen)
    def show_search(self): self.show(SearchScreen)
    def show_profile(self): self.show(StudentProfileScreen)
    def show_alerts(self): self.show(AlertsScreen)
    def show_users(self): self.show(UsersScreen)
    def show_settings(self): self.show(SettingsScreen)
    def load_predictor(self):
        if self.predictor is None:self.predictor=Predictor()
        return self.predictor
    def logout(self):
        self.current_user=None; self.predictor=None; self.last_result=None; self.last_batch_df=None; self.show_login()
