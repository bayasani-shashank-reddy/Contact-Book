import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")  # Set a light background color
        self.contacts = {}
        self.load_contacts()

        self.confirm_update_btn = None  # Button for confirming update

        title = tk.Label(root, text="Contact Book", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)

        input_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        input_frame.pack(pady=10)

        self.placeholders = {
            'name': "Name",
            'phone': "Phone",
            'email': "Email",
            'address': "Address"
        }

        # Validation command for phone entry: only digits or placeholder
        vcmd = (self.root.register(self.validate_phone), '%P')

        # Entry fields with background color
        self.name_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15, fg="grey", bg="#ffffff")
        self.name_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.name_entry, self.placeholders['name'])
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['name']))
        self.name_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['name']))

        self.phone_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15, fg="grey", bg="#ffffff", validate='key', validatecommand=vcmd)
        self.phone_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.phone_entry, self.placeholders['phone'])
        self.phone_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['phone']))
        self.phone_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['phone']))

        self.email_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20, fg="grey", bg="#ffffff")
        self.email_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.email_entry, self.placeholders['email'])
        self.email_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['email']))
        self.email_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['email']))

        self.address_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20, fg="grey", bg="#ffffff")
        self.address_entry.pack(side=tk.LEFT, padx=5)
        self.set_placeholder(self.address_entry, self.placeholders['address'])
        self.address_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.placeholders['address']))
        self.address_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.placeholders['address']))

        # Customize button colors
        self.add_btn = tk.Button(input_frame, text="Add Contact", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.add_contact)
        self.add_btn.pack(side=tk.LEFT, padx=8)

        search_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        search_frame.pack(pady=(10, 0), fill=tk.X, padx=10)
        search_label = tk.Label(search_frame, text="Search:", font=("Helvetica", 14), bg="#f0f0f0", fg="#333")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="#ffffff")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_contacts)

        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox with background color
        self.listbox = tk.Listbox(list_frame, font=("Helvetica", 14), height=20, yscrollcommand=self.scrollbar.set, bg="#ffffff", fg="#333")
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.update_contact)
        self.scrollbar.config(command=self.listbox.yview)

        buttons_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        buttons_frame.pack(pady=10)

        delete_btn = tk.Button(buttons_frame, text="Delete Contact", font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", command=self.delete_contact)
        delete_btn.pack(side=tk.LEFT, padx=5)

        update_btn = tk.Button(buttons_frame, text="Update Contact", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", command=self.update_contact)
        update_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(buttons_frame, text="Clear All", font=("Helvetica", 12, "bold"), bg="#9E9E9E", fg="white", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def validate_phone(self, new_text):
        if new_text == "" or new_text == self.placeholders['phone']:
            return True
        return new_text.isdigit()

    def set_placeholder(self, entry, placeholder):
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg="grey")

    def clear_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if name == "" or name == self.placeholders['name'] or phone == "" or phone == self.placeholders['phone']:
            messagebox.showwarning("Warning", "Name and Phone are required.")
            return

        # Add new or overwrite existing contact
        self.contacts[name] = {
            'phone': phone,
            'email': email if email != self.placeholders['email'] else '',
            'address': address if address != self.placeholders['address'] else ''
        }

        self.clear_entries()
        self.save_contacts()
        self.refresh_listbox()

        # If confirm update button was visible, remove it after add
        if self.confirm_update_btn:
            self.confirm_update_btn.destroy()
            self.confirm_update_btn = None
            self.add_btn.config(state=tk.NORMAL)

    def update_contact(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to update.")
            return
        index = selected[0]
        name = self.listbox.get(index).split(" - ")[0]
        contact = self.contacts[name]

        # Populate fields with existing contact info
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.name_entry.config(fg="black")

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact['phone'])
        self.phone_entry.config(fg="black")

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact['email'] if contact['email'] else self.placeholders['email'])
        self.email_entry.config(fg="black" if contact['email'] else "grey")

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, contact['address'] if contact['address'] else self.placeholders['address'])
        self.address_entry.config(fg="black" if contact['address'] else "grey")

        # Disable add contact button during update mode
        self.add_btn.config(state=tk.DISABLED)

        # Create and show confirm update button if it doesn't exist
        if not self.confirm_update_btn:
            self.confirm_update_btn = tk.Button(self.root, text="Confirm Update", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white",
                                                command=lambda: self.confirm_update(name))
            self.confirm_update_btn.pack(pady=5)
        else:
            # If button exists (e.g. repeated calls), just update command and text
            self.confirm_update_btn.config(text="Confirm Update", command=lambda: self.confirm_update(name))
            self.confirm_update_btn.lift()

    def confirm_update(self, old_name):
        new_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if new_name == "" or new_name == self.placeholders['name'] or phone == "" or phone == self.placeholders['phone']:
            messagebox.showwarning("Warning", "Name and Phone are required.")
            return

        if old_name != new_name and new_name in self.contacts:
            messagebox.showwarning("Warning", f"A contact named '{new_name}' already exists.")
            return

        if old_name != new_name:
            del self.contacts[old_name]

        self.contacts[new_name] = {
            'phone': phone,
            'email': email if email != self.placeholders['email'] else '',
            'address': address if address != self.placeholders['address'] else ''
        }

        self.clear_entries()
        self.save_contacts()
        self.refresh_listbox()

        if self.confirm_update_btn:
            self.confirm_update_btn.destroy()
            self.confirm_update_btn = None
            self.add_btn.config(state=tk.NORMAL)

    def delete_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        index = selected[0]
        name = self.listbox.get(index).split(" - ")[0]

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{name}'?"):
            del self.contacts[name]
            self.save_contacts()
            self.refresh_listbox()
            self.clear_entries()

            if self.confirm_update_btn:
                self.confirm_update_btn.destroy()
                self.confirm_update_btn = None
                self.add_btn.config(state=tk.NORMAL)

    def filter_contacts(self, event=None):
        search_term = self.search_entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            if search_term in name.lower() or search_term in details['phone']:
                self.listbox.insert(tk.END, f"{name} - {details['phone']}")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all contacts?"):
            self.contacts.clear()
            self.save_contacts()
            self.refresh_listbox()
            self.clear_entries()

            if self.confirm_update_btn:
                self.confirm_update_btn.destroy()
                self.confirm_update_btn = None
                self.add_btn.config(state=tk.NORMAL)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.listbox.insert(tk.END, f"{name} - {details['phone']}")

    def save_contacts(self):
        try:
            with open("contacts.txt", "w", encoding="utf-8") as f:
                for name, details in self.contacts.items():
                    email = details['email'].replace("|", "/") if details['email'] else ""
                    address = details['address'].replace("|", "/") if details['address'] else ""
                    f.write(f"{name}|{details['phone']}|{email}|{address}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {e}")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("|")
                        if len(parts) == 4:
                            name, phone, email, address = parts
                            self.contacts[name] = {'phone': phone, 'email': email, 'address': address}
                        else:
                            continue
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {e}")

    def clear_entries(self):
        self.set_placeholder(self.name_entry, self.placeholders['name'])
        self.set_placeholder(self.phone_entry, self.placeholders['phone'])
        self.set_placeholder(self.email_entry, self.placeholders['email'])
        self.set_placeholder(self.address_entry, self.placeholders['address'])


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

