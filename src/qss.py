import json


def create_qss() -> dict[str, str]:
    qss = {
        "QWidget": "QWidget { background-color: rgb(34, 34, 34); }",
        "QFrame": "QFrame { background-color: rgb(43, 43, 43); border: 1px solid rgb(56, 56, 56); border-radius: 4px; }",
        "QPushButton": "QPushButton { background-color: rgb(55, 55, 55); border: 1px solid rgb(70, 70, 70); border-radius: 4px; } QPushButton:hover { background-color: rgb(75, 75, 75); border: 1px solid rgb(90, 90, 90); } QPushButton:pressed { background-color: rgb(50, 50, 50); border: 1px solid rgb(60, 60, 60); }",
        "QLineEdit": "QLineEdit { background-color: rgb(35, 35, 35); }",
        "QLabel": "QLabel { background-color: transparent; border: none; }",
        "QDialogButtonBox": "QPushButton { background-color: rgb(55, 55, 55); border: 1px solid rgb(70, 70, 70); border-radius: 4px; height: 22px; width: 80px; } QPushButton:hover { background-color: rgb(75, 75, 75); border: 1px solid rgb(90, 90, 90); } QPushButton:pressed { background-color: rgb(50, 50, 50); border: 1px solid rgb(60, 60, 60); }"
    }

    with open("qss.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(qss, indent=4))
    return qss