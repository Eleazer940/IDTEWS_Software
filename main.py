import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    if sys.version_info < (3, 8):
        print("Python 3.8+ is required.")
        return 1

    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    try:
        from app.config import MODEL_PATH
        from app.database import init_db
        from app.gui.main_window import MainWindow

        if not os.path.exists(MODEL_PATH):
            print("Trained model not found. Running setup...")
            import setup
            if setup.main() != 0:
                return 1
    except ImportError as e:
        print("Missing package/module:", e)
        print("Run: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print("Startup error:", e)
        return 1

    try:
        init_db()
        app = MainWindow()
        app.run()
        return 0
    except Exception as e:
        print("Application error:", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
