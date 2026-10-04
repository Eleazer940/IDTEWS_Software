import os
BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
NAVY="#1B2A4A"; BLUE="#2C3E6B"; LBLUE="#3498DB"; BG="#F0F3F7"; WHITE="#FFFFFF"
GREEN="#27AE60"; RED="#C0392B"; AMBER="#E67E22"; SIDEBAR="#22313F"; LGREY="#ECF0F1"; DGREY="#7F8C8D"; BORDER="#BDC3C7"
INFO_BG="#EBF5FB"; INFO_FG="#1A5276"
CAT_COLORS={"At-Risk":RED,"Average":AMBER,"High-Achiever":GREEN}
FONT_NORMAL=("Times New Roman",11); FONT_BOLD=("Times New Roman",11,"bold"); FONT_SMALL=("Times New Roman",9); FONT_HEADING=("Times New Roman",13,"bold")
FEATURES=["attendance_pct","assignment_score","midterm_score","participation","previous_gpa"]
FEATURE_LABELS={"attendance_pct":"Attendance (%)","assignment_score":"Assignment Score (%)","midterm_score":"Midterm Score (%)","participation":"Class Participation (1-10)","previous_gpa":"Previous GPA (0.0-4.0)"}
FEATURE_RANGES={"attendance_pct":(30.,100.),"assignment_score":(20.,100.),"midterm_score":(20.,100.),"participation":(1.,10.),"previous_gpa":(0.,4.)}
MODEL_PARAMS={"criterion":"gini","max_depth":6,"min_samples_split":8,"min_samples_leaf":4,"random_state":42}
THRESHOLD_AT_RISK=57.; THRESHOLD_AVERAGE=74.; CLASSES=["At-Risk","Average","High-Achiever"]
MODEL_PATH=os.path.join(BASE_DIR,"model","idtews_model.pkl"); DB_PATH=os.path.join(BASE_DIR,"data","idtews.db"); DATA_PATH=os.path.join(BASE_DIR,"data","idtews_dataset.csv"); REPORTS_DIR=os.path.join(BASE_DIR,"reports")
RECOMMENDATIONS={"At-Risk":["Refer student for immediate academic counselling","Enrol in structured extra tutorial sessions","Develop a personalised study plan","Increase monitoring to bi-weekly check-ins","Assign a peer mentor","Notify student of risk status"],"Average":["Provide supplementary learning resources","Schedule monthly progress review","Encourage study group participation","Set short-term improvement targets","Recommend academic coaching"],"High-Achiever":["Nominate for academic excellence award","Assign peer-mentoring role","Recommend for scholarships","Encourage research participation","Provide access to advanced modules","Recognise achievement publicly"]}
APP_NAME="IDTEWS"; APP_FULL="Intelligent Decision Tree Early Warning System"; APP_DEPT="Department of Computer Science — MAU, Yola"; APP_VERSION="v4.0.0"
