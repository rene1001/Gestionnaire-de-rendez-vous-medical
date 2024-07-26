import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import sqlite3
import os
from tkcalendar import DateEntry
from typing import List, Tuple, Optional

# Configuration de la connexion à la base de données
database_path = 'appointments_db.sqlite'

def create_database_and_table() -> None:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL,
                consultation_reason TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                doctor_specialty TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Erreur lors de la création de la base de données ou de la table: {err}")

def add_appointment(date: str, time: str, patient_name: str, gender: str, age: int, consultation_reason: str, doctor_name: str, doctor_specialty: str) -> None:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (date, time, patient_name, gender, age, consultation_reason, doctor_name, doctor_specialty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, time, patient_name, gender, age, consultation_reason, doctor_name, doctor_specialty))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Erreur lors de l'ajout du rendez-vous: {err}")

def delete_appointment(appointment_id: int) -> None:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Erreur lors de la suppression du rendez-vous: {err}")

def modify_appointment(appointment_id: int, date: str, time: str, patient_name: str, gender: str, age: int, consultation_reason: str, doctor_name: str, doctor_specialty: str) -> None:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments
            SET date = ?, time = ?, patient_name = ?, gender = ?, age = ?, consultation_reason = ?, doctor_name = ?, doctor_specialty = ?
            WHERE id = ?
        ''', (date, time, patient_name, gender, age, consultation_reason, doctor_name, doctor_specialty, appointment_id))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Erreur lors de la modification du rendez-vous: {err}")

def display_appointments() -> List[Tuple]:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments')
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return appointments
    except sqlite3.Error as err:
        print(f"Erreur lors de l'affichage des rendez-vous: {err}")
        return []

def search_appointments_by_patient(patient_name: str) -> List[Tuple]:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE patient_name LIKE ?', ('%' + patient_name + '%',))
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return appointments
    except sqlite3.Error as err:
        print(f"Erreur lors de la recherche des rendez-vous par patient: {err}")
        return []

def search_appointments_by_doctor(doctor_name: str) -> List[Tuple]:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE doctor_name LIKE ?', ('%' + doctor_name + '%',))
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return appointments
    except sqlite3.Error as err:
        print(f"Erreur lors de la recherche des rendez-vous par docteur: {err}")
        return []

def generate_receipt(appointment_id: int) -> str:
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
        appointment = cursor.fetchone()
        cursor.close()
        conn.close()

        if appointment:
            receipt = f'''
            Receipt for Appointment ID: {appointment[0]}
            Patient Name: {appointment[3]}
            Appointment Date: {appointment[1]}
            Appointment Time: {appointment[2]}
            Doctor Name: {appointment[7]}
            '''
            return receipt
        else:
            return "Rendez-vous non trouvé."
    except sqlite3.Error as err:
        print(f"Erreur lors de la génération du reçu: {err}")
        return "Erreur lors de la génération du reçu."

def center_window(window: tk.Tk) -> None:
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def add_appointment_gui() -> None:
    def submit() -> None:
        date = entry_date.get()
        time = entry_time.get()
        patient_name = entry_patient_name.get()
        gender = gender_var.get()
        age = entry_age.get()
        consultation_reason = reason_var.get()
        doctor_name = entry_doctor_name.get()
        doctor_specialty = specialty_var.get()
        
        add_appointment(date, time, patient_name, gender, int(age), consultation_reason, doctor_name, doctor_specialty)
        messagebox.showinfo("Succès", "Rendez-vous ajouté avec succès")

    window = tk.Tk()
    window.title("Ajouter un nouveau rendez-vous")
    window.geometry('700x500')
    window.config(bg='green')

    center_window(window)

    form_frame = tk.Frame(window, bg='green')
    form_frame.pack(expand=True)

    tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=0, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Heure (HH:MM)", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=1, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Nom du patient", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=2, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Genre", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=3, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Âge", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=4, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Raison de consultation", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=5, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Nom du médecin", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=6, column=0, pady=8, padx=5, sticky='w')
    tk.Label(form_frame, text="Spécialité du médecin", bg='green', fg='white', font=('Arial', 15, 'bold')).grid(row=7, column=0, pady=8, padx=5, sticky='w')

    entry_date = DateEntry(form_frame, width=38, background='darkblue', foreground='white', borderwidth=2)
    entry_time = tk.Entry(form_frame, width=40)
    entry_patient_name = tk.Entry(form_frame, width=40)
    gender_var = tk.StringVar(value='Homme')
    entry_age = tk.Entry(form_frame, width=40)
    reason_var = tk.StringVar(value='MALADE')
    entry_doctor_name = tk.Entry(form_frame, width=40)
    specialty_var = tk.StringVar(value='GENICOLOGUE')
    
    entry_date.grid(row=0, column=1, pady=5, padx=5)
    entry_time.grid(row=1, column=1, pady=5, padx=5)
    entry_patient_name.grid(row=2, column=1, pady=5, padx=5)
    
    gender_menu = ttk.Combobox(form_frame, textvariable=gender_var, values=['Homme', 'Femme'], width=38)
    gender_menu.grid(row=3, column=1, pady=5, padx=5)
    
    entry_age.grid(row=4, column=1, pady=5, padx=5)
    
    reason_menu = ttk.Combobox(form_frame, textvariable=reason_var, values=['MALADE', 'MAUX DE TETE', 'CANCERS'], width=38)
    reason_menu.grid(row=5, column=1, pady=5, padx=5)
    
    entry_doctor_name.grid(row=6, column=1, pady=5, padx=5)
    
    specialty_menu = ttk.Combobox(form_frame, textvariable=specialty_var, values=['GENICOLOGUE', 'GENERALISTE', 'MEDECIN'], width=38)
    specialty_menu.grid(row=7, column=1, pady=5, padx=5)
    
    tk.Button(form_frame, text="Ajouter", command=submit, bg='blue', fg='white', font=('Arial', 15, 'bold')).grid(row=8, column=0, columnspan=5, pady=14)
    
    window.mainloop()

def display_appointments_gui() -> None:
    appointments = display_appointments()
    window = tk.Tk()
    window.title("Tous les Rendez-vous")
    window.geometry('900x500')
    window.config(bg='white')

    center_window(window)

    tk.Label(window, text="Nom", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Date", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=1, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Heure", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=2, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Genre", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=3, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Âge", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=4, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Raison de consultation", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=5, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Nom du docteur", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=6, padx=10, pady=5, sticky='w')
    tk.Label(window, text="Spécialité du docteur", font=("Arial", 10, "bold"), bg='white').grid(row=0, column=7, padx=10, pady=5, sticky='w')

    for idx, appointment in enumerate(appointments):
        tk.Label(window, text=appointment[3], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[1], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=1, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[2], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=2, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[4], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=3, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[5], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=4, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[6], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=5, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[7], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=6, padx=10, pady=5, sticky='w')
        tk.Label(window, text=appointment[8], font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=7, padx=10, pady=5, sticky='w')

    window.mainloop()

def delete_appointment_gui() -> None:
    def search_and_delete() -> None:
        patient_name = entry_patient_name.get()
        if patient_name:
            appointments = search_appointments_by_patient(patient_name)
            if not appointments:
                messagebox.showinfo("Info", "Aucun rendez-vous trouvé pour ce patient.")
                return

            def delete_selected_appointment() -> None:
                selected_item = appointment_listbox.curselection()
                if not selected_item:
                    messagebox.showwarning("Avertissement", "Veuillez sélectionner un rendez-vous à supprimer.")
                    return

                appointment_id = appointments[selected_item[0]][0]
                delete_appointment(appointment_id)
                messagebox.showinfo("Succès", "Rendez-vous supprimé avec succès")
                window.destroy()

            window = tk.Toplevel()
            window.title("Supprimer un Rendez-vous")
            window.geometry('500x400')
            window.config(bg='green')
            center_window(window)

            tk.Label(window, text="Sélectionnez le rendez-vous à supprimer :", bg='green', fg='white', font=('Arial', 12)).pack(pady=10)

            appointment_listbox = tk.Listbox(window, width=80)
            appointment_listbox.pack(pady=10)

            for appointment in appointments:
                appointment_listbox.insert(tk.END, f"{appointment[0]} - {appointment[3]} - {appointment[1]} - {appointment[2]}")

            tk.Button(window, text="Supprimer", command=delete_selected_appointment, bg='blue', fg='white').pack(pady=10)

    window = tk.Tk()
    window.title("Supprimer un rendez-vous")
    window.geometry('400x200')
    window.config(bg='green')
    center_window(window)

    tk.Label(window, text="Entrez le nom du patient :", bg='green', fg='white').pack(pady=10)
    entry_patient_name = tk.Entry(window, width=40)
    entry_patient_name.pack(pady=10)
    tk.Button(window, text="Rechercher et supprimer", command=search_and_delete, bg='blue', fg='white').pack(pady=10)

    window.mainloop()

def modify_appointment_gui() -> None:
    patient_name = CustomStringDialog("Entrée", "Entrez le nom du patient pour modifier ses rendez-vous").result
    if patient_name:
        appointments = search_appointments_by_patient(patient_name)
        if not appointments:
            messagebox.showinfo("Info", "Aucun rendez-vous trouvé pour ce patient.")
            return

        def submit() -> None:
            appointment_id = appointment_var.get()
            date = entry_date.get()
            time = entry_time.get()
            patient_name = entry_patient_name.get()
            gender = gender_var.get()
            age = entry_age.get()
            consultation_reason = reason_var.get()
            doctor_name = entry_doctor_name.get()
            doctor_specialty = specialty_var.get()
            
            modify_appointment(appointment_id, date, time, patient_name, gender, int(age), consultation_reason, doctor_name, doctor_specialty)
            messagebox.showinfo("Succès", "Rendez-vous modifié avec succès")

        window = tk.Tk()
        window.title("Modifier un rendez-vous")
        window.geometry('400x500')
        window.config(bg='lightgreen')

        center_window(window)

        form_frame = tk.Frame(window, bg='green')
        form_frame.pack(expand=True)

        tk.Label(form_frame, text="Rendez-vous ID", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=1, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Heure (HH:MM)", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=2, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Nom du patient", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=3, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Genre", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=4, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Âge", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=5, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Raison de consultation", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=6, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Nom du médecin", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=7, column=0, pady=5, padx=5, sticky='w')
        tk.Label(form_frame, text="Spécialité du médecin", bg='green', fg='white', font=('Arial', 10, 'bold')).grid(row=8, column=0, pady=5, padx=5, sticky='w')

        appointment_var = tk.IntVar()
        appointment_menu = ttk.Combobox(form_frame, textvariable=appointment_var, values=[appointment[0] for appointment in appointments], width=28)
        appointment_menu.grid(row=0, column=1, pady=5, padx=5)

        entry_date = DateEntry(form_frame, width=28, background='darkblue', foreground='white', borderwidth=2)
        entry_time = tk.Entry(form_frame, width=30)
        entry_patient_name = tk.Entry(form_frame, width=30)
        gender_var = tk.StringVar(value='Homme')
        entry_age = tk.Entry(form_frame, width=30)
        reason_var = tk.StringVar(value='MALADE')
        entry_doctor_name = tk.Entry(form_frame, width=30)
        specialty_var = tk.StringVar(value='GENICOLOGUE')
        
        entry_date.grid(row=1, column=1, pady=5, padx=5)
        entry_time.grid(row=2, column=1, pady=5, padx=5)
        entry_patient_name.grid(row=3, column=1, pady=5, padx=5)
        
        gender_menu = ttk.Combobox(form_frame, textvariable=gender_var, values=['Homme', 'Femme'], width=28)
        gender_menu.grid(row=4, column=1, pady=5, padx=5)
        
        entry_age.grid(row=5, column=1, pady=5, padx=5)
        
        reason_menu = ttk.Combobox(form_frame, textvariable=reason_var, values=['MALADE', 'MAUX DE TETE', 'CANCERS'], width=28)
        reason_menu.grid(row=6, column=1, pady=5, padx=5)
        
        entry_doctor_name.grid(row=7, column=1, pady=5, padx=5)
        
        specialty_menu = ttk.Combobox(form_frame, textvariable=specialty_var, values=['GENICOLOGUE', 'GENERALISTE', 'MEDECIN'], width=28)
        specialty_menu.grid(row=8, column=1, pady=5, padx=5)

        tk.Button(form_frame, text="Soumettre", command=submit, bg='blue', fg='white').grid(row=9, column=0, columnspan=2, pady=10)
        
        window.mainloop()

def search_appointments_gui() -> None:
    def search_by_patient() -> None:
        patient_name = CustomStringDialog("Entrée", "Entrez le nom du patient à rechercher").result
        if patient_name:
            appointments = search_appointments_by_patient(patient_name)
            show_search_results(appointments)

    def search_by_doctor() -> None:
        doctor_name = CustomStringDialog("Entrée", "Entrez le nom du médecin à rechercher").result
        if doctor_name:
            appointments = search_appointments_by_doctor(doctor_name)
            show_search_results(appointments)

    window = tk.Tk()
    window.title("Rechercher des Rendez-vous")
    window.geometry('400x300')
    window.config(bg='lightgreen')

    center_window(window)

    tk.Button(window, text="Rechercher par nom de patient", command=search_by_patient, bg='white').pack(pady=10)
    tk.Button(window, text="Rechercher par nom de médecin", command=search_by_doctor, bg='white').pack(pady=10)

    window.mainloop()

def show_search_results(appointments: List[Tuple]) -> None:
    window = tk.Tk()
    window.title("Résultats de la Recherche")
    window.geometry('900x200')
    window.config(bg='white')  # Set the background color to light green

    center_window(window)

    # Creating headers
    headers = ["ID", "Date", "Heure", "Nom du patient", "Genre", "Âge", "Raison de consultation", "Nom du docteur", "Spécialité du docteur"]

    # Adding headers in a horizontal layout
    for col, header in enumerate(headers):
        tk.Label(window, text=header, font=("Arial", 10, "bold"), bg='white').grid(row=0, column=col, padx=10, pady=5, sticky='w')

    # Adding appointment details
    for idx, appointment in enumerate(appointments):
        for col, value in enumerate(appointment):
            tk.Label(window, text=value, font=("Arial", 10, "italic"), bg='white').grid(row=idx + 1, column=col, padx=10, pady=5, sticky='w')

    window.mainloop()

class CustomStringDialog(simpledialog.Dialog):
    def __init__(self, title: str, prompt: str) -> None:
        self.prompt = prompt
        super().__init__(parent=None, title=title)

    def body(self, master: tk.Frame) -> tk.Widget:
        self.configure(bg='lightgreen')
        tk.Label(master, text=self.prompt, bg='lightgreen').pack(pady=10)
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=10)
        return self.entry

    def apply(self) -> None:
        self.result = self.entry.get()

def main_gui() -> None:
    window = tk.Tk()
    window.title("Gestionnaire des Rendez-vous du Clinic")
    window.geometry('700x800')

    center_window(window)

    # Ajouter un canevas pour l'image de fond
    canvas = tk.Canvas(window, width=700, height=800)
    canvas.pack(fill="both", expand=True)

    # Charger l'image de fond
    bg_image_path = r"background.png"
    if os.path.exists(bg_image_path):
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((2000, 800), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    else:
        messagebox.showwarning("Avertissement", "Image de fond non trouvée.")

    # Charger le logo
    logo_image_path = r"logo_circle1.png"  # Mettez le chemin correct ici
    if os.path.exists(logo_image_path):
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((80, 80), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
    else:
        logo_photo = None
        messagebox.showwarning("Avertissement", "Logo non trouvé.")

    # Ajouter les widgets sur le canevas
    top_bar = tk.Frame(canvas, bg='green', height=100, width=500)
    top_bar.pack(fill=tk.X)

    if logo_photo:
        logo_label = tk.Label(top_bar, image=logo_photo, bg='green')
        logo_label.pack(side=tk.LEFT, padx=10)
        logo_label.image = logo_photo  # Pour s'assurer que l'image reste affichée

    tk.Label(top_bar, text="Gestionnaire des Rendez-vous du Clinic", font=("Arial", 30), fg="white", bg="green", anchor="center").pack(pady=20)

    sidebar = tk.Frame(canvas, bg='lightgreen', height=500, width=200)
    sidebar.pack(fill=tk.Y, side=tk.LEFT, pady=5)

    # Adapter les boutons avec padx pour l'espacement à gauche
    tk.Button(sidebar, text="AJOUTER", command=add_appointment_gui, bg='white').pack(pady=20, padx=60)
    tk.Button(sidebar, text="SUPPRIMER", command=delete_appointment_gui, bg='white').pack(pady=20, padx=60)
    tk.Button(sidebar, text="MODIFIER", command=modify_appointment_gui, bg='white').pack(pady=20, padx=60)
    tk.Button(sidebar, text="AFFICHER", command=display_appointments_gui, bg='white').pack(pady=20, padx=60)
    tk.Button(sidebar, text="Rechercher des rendez-vous", command=search_appointments_gui, bg='white').pack(pady=20, padx=20)
    

    window.mainloop()

if __name__ == '__main__':
    create_database_and_table()
    main_gui()
