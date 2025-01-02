import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime

root = tk.Tk()
root.geometry("700x500+1550+100")

def calculate_days():
    start_data = start_date_entry.get_date()
    end_data = end_date_entry.get_date()
    print(start_data)
    print(end_data)
    delta = end_data - start_data


    result_label.config(text=f"金利発生日: {delta.days} 日")


tk.Label(root, text="銘柄コード").grid(row=0, column=1)


tk.Label(root, text="注文日").grid(row=1, column=1)
start_date_entry = DateEntry(root, year=2024, locale='ja_JP')
start_date_entry.grid(row=1, column=2)

tk.Label(root,text="権利確定日").grid(row=1, column=3, padx=(10,0))
end_date_entry = DateEntry(root, year=2024, locale='ja_JP')
end_date_entry.grid(row=1, column=4,)

button = tk.Button(root, text="計算", command=calculate_days)
button.grid(row=2,column=0,columnspan=4, pady=10)

result_label = tk.Label(root, text = "")
result_label.grid(row=3, column=0, columnspan=2)

import subprocess
from dotenv import load_dotenv
import os
print(os.getcwd())

def run_script():
    print("書き込み開始")
    start_data = start_date_entry.get_date().strftime("%Y%m%d")
    end_data = end_date_entry.get_date().strftime("%Y%m%d")
    venv_python = r"C:\Users\yumib\Desktop\dev\python\dev\GUI\.venv\Scripts\python"
    subprocess.run([venv_python, "jquants.py", start_data, end_data], env=os.environ.copy(), cwd=os.getcwd())
    print("終了")


run_button = tk.Button(root, text="書き込み", command=run_script)
run_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
