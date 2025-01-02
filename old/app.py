import tkinter as tk
from tkinter import Pack, filedialog, Text
import os
import pathlib

root = tk.Tk()
root.geometry("700x500+1550+100")
apps = []

def addApp():
    for widget in frame.winfo_children():
        widget.destroy()

    #ファイルを選択する画面を開く
    filename = filedialog.askopenfilename(initialdir="/",
        filetypes=(("exexutables", "*.exe"),("all files", "*.*")))
    
    # 開いたファイルの名前をappsに格納、appsに入ったファイル名を表示する
    apps.append(filename)
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()

def runApps():
    for app in apps:
        os.startfile(app)
    

def deleteApps():
    apps.clear()
    for widget in frame.winfo_children():
        widget.destroy()

#アプリの大きさや背景色を設定する
# canvas = tk.Canvas(width=600, height=400, bg="#263D42")
# canvas.pack()

#フレーム（内枠を作成）
frame = tk.Frame(root, bg="red", width=500, height=200)
frame.pack(fill="x")

frame2 = tk.Frame(root, bg="white", width=500, height=200)
frame2.pack(pady=10, fill="x")

def submit():
    print('ボタンが押されました')
    t = text.get(1.0, tk.END + '-1c')
    print(t)


text = tk.Text(frame, width=20, height=10)
text.pack(pady=(10,10))

button = tk.Button(frame, text="実行", command=submit)
button.pack()
# ボタンを作成 pad…パディング、fg…フォントカラー
openFileButton = tk.Button(frame2, text="Open File", padx=10, pady=10, fg="white", bg="#263D42", command=addApp)
openFileButton.pack()

runFileButton = tk.Button(frame2, text="Run File", padx=10, pady=10, fg="white", bg="#263D42", command=runApps)
runFileButton.pack()

deleteFileButton = tk.Button(root, text="Delete File", padx=10, pady=10, fg="white", bg="#263D42", command=deleteApps)
deleteFileButton.pack()



















root.mainloop()
