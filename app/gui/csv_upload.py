import os
import shutil
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.config import (
    BG, NAVY, BLUE, WHITE, FEATURES, FONT_NORMAL, FONT_HEADING
)
from app.modules.reporter import Reporter
from app.database import save_batch_predictions, save_uploaded_file


class CsvUploadScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.pack(fill="both", expand=True)

        self.controller = controller
        self.df = None
        self.original_path = None
        self.saved = False

        make_header(self, controller, "CSV Upload")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        Sidebar(body, controller, "upload")

        content = tk.Frame(body, bg=BG, padx=15, pady=12)
        content.pack(side="left", fill="both", expand=True)

        buttons = tk.Frame(content, bg=BG)
        buttons.pack(fill="x", pady=(0, 8))

        tk.Button(
            buttons,
            text="BROWSE CSV",
            command=self.open_csv,
            bg=NAVY,
            fg=WHITE,
            font=FONT_NORMAL,
        ).pack(side="left", padx=(0, 6))

        self.save_button = tk.Button(
            buttons,
            text="SAVE UPLOAD",
            command=self.save_upload,
            bg="#27AE60",
            fg=WHITE,
            font=FONT_NORMAL,
            state="disabled",
        )
        self.save_button.pack(side="left", padx=6)

        tk.Button(
            buttons,
            text="EXPORT REPORT",
            command=self.export_report,
            bg=BLUE,
            fg=WHITE,
            font=FONT_NORMAL,
        ).pack(side="right")

        self.info = tk.Label(
            content, text="", bg=BG, fg=NAVY, font=FONT_HEADING
        )
        self.info.pack(anchor="w", pady=8)

        cols = ["student_id"] + FEATURES + [
            "predicted_class", "confidence"
        ]

        self.table = ttk.Treeview(
            content,
            columns=cols,
            show="headings",
            height=18,
        )

        for column in cols:
            self.table.heading(column, text=column)
            self.table.column(column, width=115, anchor="center")

        self.table.pack(fill="both", expand=True)

        self.table.tag_configure("At-Risk", background="#F5B7B1")
        self.table.tag_configure("Average", background="#FAD7A0")
        self.table.tag_configure("High-Achiever", background="#ABEBC6")

    def open_csv(self):
        path = filedialog.askopenfilename(
            title="Select Student CSV File",
            filetypes=[("CSV files", "*.csv")],
        )

        if not path:
            return

        try:
            data = pd.read_csv(path)
            missing = [x for x in FEATURES if x not in data.columns]

            if missing:
                raise ValueError(
                    "Missing required columns: " + ", ".join(missing)
                )

            predictor = self.controller.load_predictor()

            data = data.copy()
            if "student_id" not in data.columns:
                data.insert(
                    0,
                    "student_id",
                    [f"CSV-{i + 1:04d}" for i in range(len(data))],
                )

            self.df = predictor.predict_batch(data)
            self.original_path = path
            self.saved = False
            self.controller.last_batch_df = self.df

            self.display_data()
            self.update_info()
            self.save_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

    def display_data(self):
        for item in self.table.get_children():
            self.table.delete(item)

        if self.df is None:
            return

        columns = self.table["columns"]

        for _, row in self.df.iterrows():
            values = []
            for column in columns:
                value = row.get(column, "")
                if column == "confidence":
                    value = f"{float(value):.2f}"
                values.append(value)

            self.table.insert(
                "",
                "end",
                values=values,
                tags=(str(row["predicted_class"]),),
            )

    def update_info(self):
        if self.df is None:
            return

        counts = self.df["predicted_class"].value_counts()

        saved_text = " | SAVED" if self.saved else " | NOT SAVED"

        self.info.config(
            text=(
                f"Processed {len(self.df)} students | "
                f"At-Risk {counts.get('At-Risk', 0)} | "
                f"Average {counts.get('Average', 0)} | "
                f"High-Achiever {counts.get('High-Achiever', 0)}"
                f"{saved_text}"
            )
        )

    def save_upload(self):
        """Save the uploaded CSV and all generated predictions permanently."""
        if self.df is None or self.original_path is None:
            messagebox.showwarning(
                "Save Upload",
                "Please browse and process a CSV file first.",
            )
            return

        if self.saved:
            messagebox.showinfo(
                "Already Saved",
                "This uploaded CSV has already been saved.",
            )
            return

        try:
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            uploads_dir = os.path.join(
                project_root, "data", "uploads"
            )
            os.makedirs(uploads_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(self.original_path)
            stem, extension = os.path.splitext(original_name)

            original_copy = os.path.join(
                uploads_dir,
                f"{stem}_{timestamp}{extension}",
            )
            shutil.copy2(self.original_path, original_copy)

            predicted_copy = os.path.join(
                uploads_dir,
                f"{stem}_{timestamp}_predicted.csv",
            )
            self.df.to_csv(predicted_copy, index=False)

            saved_rows = save_batch_predictions(self.df)
            save_uploaded_file(
                original_name,
                original_copy,
                saved_rows,
            )

            self.saved = True
            self.update_info()
            self.save_button.config(state="disabled")

            messagebox.showinfo(
                "Upload Saved",
                (
                    f"Successfully saved {saved_rows} student predictions.\n\n"
                    f"Original CSV:\n{original_copy}\n\n"
                    f"Predicted CSV:\n{predicted_copy}\n\n"
                    "The Dashboard will now show the saved data."
                ),
            )

        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def export_report(self):
        if self.df is None:
            messagebox.showwarning(
                "Export",
                "No CSV data has been processed yet.",
            )
            return

        try:
            path = Reporter.export_csv(self.df)
            messagebox.showinfo(
                "Export Complete",
                f"Report saved successfully:\n{path}",
            )
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
