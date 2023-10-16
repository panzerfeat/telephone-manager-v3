import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


conn = sqlite3.connect("phonebook.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)"
)
conn.commit()


def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name and phone and email:
        cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email),
        )
        conn.commit()
        messagebox.showinfo("Success", "Контакт успешно добавлен.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Пожалуйста, заполните все поля.")

def show_contacts():
    contacts_tree.delete(*contacts_tree.get_children())

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    for contact in contacts:
        contact_id = contact[0]
        name = contact[1]
        phone = contact[2]
        email = contact[3]
        contacts_tree.insert("", "end", text=contact_id, values=(name, phone, email))        


def update_contact():
    selected_contact = contacts_tree.selection()

    if selected_contact:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if name and phone and email:
            contact_id = contacts_tree.item(selected_contact)["text"]
            cursor.execute(
                "UPDATE contacts SET name=?, phone=?, email=? WHERE id=?",
                (name, phone, email, contact_id),
            )
            conn.commit()
            messagebox.showinfo("Success", "Контакт успешно обновлен.")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            show_contacts()
        else:
            messagebox.showerror("Error", "Пожалуйста, выберите контакт и заполните все поля.")
    else:
        messagebox.showerror("Error", "Пожалуйста, выберите контакт для обновления.")


def delete_contact():
    selected_contact = contacts_tree.selection()

    if selected_contact:
        confirmed = messagebox.askyesno(
            "Confirm", "Вы уверены, что хотите удалить выбранный контакт?"
        )
        if confirmed:
            contact_id = contacts_tree.item(selected_contact)["text"]
            cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            conn.commit()
            messagebox.showinfo("Success", "Контакт успешно удален.")
            show_contacts()
    else:
        messagebox.showerror("Error", "Пожалуйста, выберите контакт для удаления.")


def search_contacts():
    search_name = search_entry.get()

    cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", (f"%{search_name}%",))
    contacts = cursor.fetchall()

    contacts_tree.delete(*contacts_tree.get_children())

    for contact in contacts:
        contacts_tree.insert(
            "",
            tk.END,
            text=contact[0],
            values=(contact[1], contact[2], contact[3]),
        )


def show_contacts():
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    contacts_tree.delete(*contacts_tree.get_children())

    for contact in contacts:
        contacts_tree.insert(
            "",
            tk.END,
            text=contact[0],
            values=(contact[1], contact[2], contact[3]),
        )



root = tk.Tk()
root.title("Телефонная книга")


input_frame = tk.LabelFrame(root, text="Введите данные контакта")
input_frame.pack(padx=10, pady=10)

name_label = tk.Label(input_frame, text="ФИО:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = tk.Label(input_frame, text="Телефон:")
phone_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

phone_entry = tk.Entry(input_frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = tk.Label(input_frame, text="Email:")
email_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

email_entry = tk.Entry(input_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Добавить", command=add_contact)
add_button.pack(pady=5)

update_button = tk.Button(root, text="Обновить", command=update_contact)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Удалить", command=delete_contact)
delete_button.pack(pady=5)


search_frame = tk.LabelFrame(root, text="Поиск по ФИО")
search_frame.pack(padx=10, pady=10)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Поиск", command=search_contacts)
search_button.pack(side=tk.LEFT, padx=5, pady=5)


contacts_frame = tk.Frame(root)
contacts_frame.pack(padx=10, pady=10)

contacts_tree = ttk.Treeview(
    contacts_frame,
    columns=("name", "phone", "email"),
    show="headings",
)

contacts_tree.heading("name", text="ФИО")
contacts_tree.heading("phone", text="Телефон")
contacts_tree.heading("email", text="Email")

contacts_tree.column("name", width=200)
contacts_tree.column("phone", width=150)
contacts_tree.column("email", width=200)

contacts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

contacts_scroll = ttk.Scrollbar(contacts_frame, orient=tk.VERTICAL, command=contacts_tree.yview)
contacts_scroll.pack(side=tk.RIGHT, fill=tk.Y)

contacts_tree.configure(yscrollcommand=contacts_scroll.set)

show_contacts()

root.mainloop()


cursor.close()
conn.close()