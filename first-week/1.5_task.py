import tkinter as tk
from tkinter import scrolledtext
import datetime

# Создаем основное окно
root = tk.Tk()
root.title("Чат")
root.configure(bg="#f0f0f0")
root.resizable(width=False,height=False)

# Область для сообщений
chat_area = scrolledtext.ScrolledText(root, width=50, height=20, bg="#ffffff", fg="#000000", font=("Arial", 12), wrap=tk.WORD)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
chat_area.config(state='disabled')

# Настраиваем цвета для пользователей
chat_area.tag_configure("user1", foreground="blue")
chat_area.tag_configure("user2", foreground="red")

# Поле для ввода
message_entry = tk.Entry(root, width=40, bg="#ffffff", fg="#000000", font=("Arial", 12))
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Кнопка "Отправить"
send_button = tk.Button(root, text="Отправить", bg="#4CAF50", fg="#ffffff", font=("Arial", 12))
send_button.grid(row=1, column=1, padx=10, pady=10)

# Переменная для текущего пользователя
current_user = "Пользователь 1"

# Кнопки для переключения пользователей
user1_button = tk.Button(root, text="Пользователь 1", command=lambda: set_user("Пользователь 1"), bg="#2196F3", fg="#ffffff", font=("Arial", 12))
user1_button.grid(row=2, column=0, padx=10, pady=10)

user2_button = tk.Button(root, text="Пользователь 2", command=lambda: set_user("Пользователь 2"), bg="#FF5722", fg="#ffffff", font=("Arial", 12))
user2_button.grid(row=2, column=1, padx=10, pady=10)

# Функция для переключения пользователей
def set_user(user):
    global current_user
    current_user = user

# Функция отправки сообщения
def send_message():
    message = message_entry.get()
    if message:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {current_user}: {message}\n"
        
        chat_area.config(state='normal')
        if current_user == "Пользователь 1":
            chat_area.insert(tk.END, full_message, "user1")
        else:
            chat_area.insert(tk.END, full_message, "user2")
        chat_area.config(state='disabled')
        
        chat_area.see(tk.END)
        message_entry.delete(0, tk.END)

# Привязка кнопки
send_button.config(command=send_message)

# Отправка сообщения при нажатии на Enter
def send_message_event(event):
    send_message()

message_entry.bind("<Return>", send_message_event)

root.mainloop()