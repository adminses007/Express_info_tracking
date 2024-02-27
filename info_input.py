import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS express (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT UNIQUE,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_express_info(tracking_number, status):
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO express (tracking_number, status) VALUES (?, ?)', (tracking_number, status))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("错误", "快递单号已存在。")
        return False
    finally:
        conn.close()

def delete_express_info(tracking_number):
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM express WHERE tracking_number = ?', (tracking_number,))
    if cursor.rowcount == 0:
        messagebox.showwarning("警告", "未找到该快递单号。")
    else:
        messagebox.showinfo("成功", "快递信息已删除。")
    conn.commit()
    conn.close()

def search_express_info(tracking_number):
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tracking_number, status FROM express WHERE tracking_number = ?', (tracking_number,))
    result = cursor.fetchone()
    conn.close()
    if result:
        messagebox.showinfo("搜索结果", f"快递单号: {result[0]}, 状态: {result[1]}")
    else:
        messagebox.showerror("错误", "未找到该快递单号的信息。")

def add_info(entry_tracking_number, entry_status, text_area):
    tracking_number = entry_tracking_number.get()
    status = entry_status.get()
    if tracking_number and status:
        if add_express_info(tracking_number, status):
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"快递单号: {tracking_number}, 状态: {status}\n")
            text_area.config(state=tk.DISABLED)
        entry_tracking_number.delete(0, tk.END)
        entry_status.delete(0, tk.END)
    else:
        messagebox.showwarning("警告", "请输入快递单号和状态。")

def delete_info(entry_tracking_number, entry_status, text_area):
    tracking_number = entry_tracking_number.get()
    if tracking_number:
        delete_express_info(tracking_number)
        entry_tracking_number.delete(0, tk.END)
        entry_status.delete(0, tk.END)
    else:
        messagebox.showwarning("警告", "请输入要删除的快递单号。")
    refresh_text_area(text_area)

def search_info(entry_tracking_number, text_area):
    tracking_number = entry_tracking_number.get()
    if tracking_number:
        search_express_info(tracking_number)
        entry_tracking_number.delete(0, tk.END)
    else:
        messagebox.showwarning("警告", "请输入要搜索的快递单号。")

def refresh_text_area(text_area):
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    conn = sqlite3.connect('express_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tracking_number, status FROM express')
    for row in cursor.fetchall():
        text_area.insert(tk.END, f"快递单号: {row[0]}, 状态: {row[1]}\n")
    conn.close()
    text_area.config(state=tk.DISABLED)

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "#123456":
        messagebox.showinfo("登录成功", "欢迎回来，管理员!")
        rootw.destroy()
        create_main_window()
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")

def create_main_window():
    root = tk.Tk()
    root.title("瑞达快递信息管理系统")
    root.iconbitmap('express_ico.ico')
    root.configure(bg="#ADD8E6")

    screen_width = 600
    screen_height = 600
    root.geometry("{}x{}+{}+{}".format(screen_width, screen_height,
                                       (root.winfo_screenwidth() - screen_width) // 2,
                                       (root.winfo_screenheight() - screen_height) // 2))
    root.resizable(False, False)

    root.attributes('-alpha', 0.9)

    frame = tk.Frame(root,bg="#ADD8E6")
    frame.pack(padx=10, pady=10)

    label_tracking_number = tk.Label(frame, text="快递单号:",highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.RIDGE)
    label_tracking_number.pack(side=tk.LEFT)
    entry_tracking_number = tk.Entry(frame,highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6")
    entry_tracking_number.pack(side=tk.LEFT)

    label_status = tk.Label(frame, text="状态:",highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.RIDGE)
    label_status.pack(side=tk.LEFT)
    entry_status = tk.Entry(frame,highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6")
    entry_status.pack(side=tk.LEFT)

    button_add = tk.Button(frame, text="添加信息", command=lambda: add_info(entry_tracking_number, entry_status, text_area),highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.GROOVE)
    button_add.pack(side=tk.LEFT, padx=5)

    button_delete = tk.Button(frame, text="删除信息", command=lambda: delete_info(entry_tracking_number, entry_status, text_area),highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.GROOVE)
    button_delete.pack(side=tk.LEFT, padx=5)

    button_search = tk.Button(frame, text="搜索信息", command=lambda: search_info(entry_tracking_number, text_area),highlightbackground="orange", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.GROOVE)
    button_search.pack(side=tk.LEFT, padx=5)

    text_area = scrolledtext.ScrolledText(root, width=80, height=50,bg="#ADD8E6")
    text_area.pack(padx=10, pady=5)
    text_area.config(state=tk.DISABLED)

    refresh_text_area(text_area)

    root.mainloop()

init_db()

rootw = tk.Tk()
rootw.title("瑞达快递信息系统")
rootw.configure(bg="#ADD8E6")
rootw.iconbitmap('express_ico.ico')

rootw.resizable(False, False)

label_username = tk.Label(rootw, text="用户名:", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.RIDGE)
label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(rootw,justify="center", fg="black", highlightcolor="orange",bg="#ADD8E6")
entry_username.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(rootw, text="密码:", highlightcolor="orange",bg="#ADD8E6", borderwidth=2, relief=tk.RIDGE)
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(rootw, show="*",justify="center", fg="black", highlightcolor="orange",bg="#ADD8E6")
entry_password.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(rootw, text="登录", command=login, highlightcolor="orange",bg="#ADD8E6", width=10, borderwidth=2, relief=tk.GROOVE)
login_button.grid(row=0, column=2,columnspan=5, pady=10)

exit_button = tk.Button(rootw, text="退出", command=exit, highlightcolor="orange",bg="#ADD8E6", width=10, borderwidth=2, relief=tk.GROOVE)
exit_button.grid(row=1, column=2,columnspan=5, pady=10)

screen_width = rootw.winfo_screenwidth()
screen_height = rootw.winfo_screenheight()

window_width = 320
window_height = 100
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

rootw.geometry(f"{window_width}x{window_height}+{x}+{y}")
rootw.attributes('-alpha', 0.9)

rootw.mainloop()
