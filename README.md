# IDTEWS Software

## Intelligent Decision Tree-Based Early Warning System

A Python/Tkinter desktop application for predicting student academic performance using a CART Decision Tree classifier.

### Main Features
- User login
- Manual student data entry
- Single-student prediction
- CSV batch upload
- Permanent CSV upload saving
- Automatic batch prediction
- SQLite database storage
- Analytics dashboard
- Risk distribution charts
- Feature importance chart
- Recent prediction history
- CSV report export
- PDF prediction report export

### Required CSV Columns
```text
attendance_pct
assignment_score
midterm_score
participation
previous_gpa
```

Optional:
```text
student_id
```

If `student_id` is not included, IDTEWS automatically creates IDs such as `CSV-0001`.

### Installation

Open Command Prompt inside the `IDTEWS_Software` folder and run:

```cmd
pip install -r requirements.txt
python setup.py
python main.py
```

### Default Login Accounts

- Admin
  - Username: `admin`
  - Password: `admin123`

- Lecturer
  - Username: `lecturer01`
  - Password: `pass1234`

- Adviser
  - Username: `adviser01`
  - Password: `pass1234`

### CSV Saving

After uploading and processing a CSV:

1. Click **SAVE UPLOAD**
2. The original CSV is copied to:
   `data/uploads/`
3. A predicted version of the CSV is also saved there.
4. All predictions are saved permanently in:
   `data/idtews.db`
5. Open **Dashboard** to view the saved predictions.

### Run

```cmd
python main.py
```
