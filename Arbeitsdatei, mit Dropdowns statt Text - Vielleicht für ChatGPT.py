from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import sqlite3


KV = '''
ScreenManager:
    id: screen_manager

    MDScreen:
        name: 'welcome_screen'
        BoxLayout:
            orientation: 'vertical'
            padding: '32dp'
            spacing: '20dp'

            Label:
                text: 'Willkommen!'
                font_size: '24sp'
                halign: 'center'

            MDRaisedButton:
                text: 'Registrieren'
                pos_hint: {'center_x': 0.5}
                on_release: app.on_welcome_button('register')
                
            MDRaisedButton:
                text: 'Anmelden'
                pos_hint: {'center_x': 0.5}
                on_release: app.on_welcome_button('login')

    MDScreen:
        name: 'register_screen'
        MDTextField:
            id: username_field
            hint_text: 'Benutzername'
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}

        MDTextField:
            id: password_field
            hint_text: 'Passwort'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            password: True

        MDRaisedButton:
            text: 'Registrieren'
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            on_release: app.on_register(*args)

        MDRaisedButton:
            text: 'Zurück'
            pos_hint: {'center_x': 0.1, 'center_y': 0.95}
            on_release: app.on_back_button()

    MDScreen:
        name: 'login_screen'
        MDTextField:
            id: login_username_field
            hint_text: 'Benutzername'
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}

        MDTextField:
            id: login_password_field
            hint_text: 'Passwort'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            password: True

        MDRaisedButton:
            text: 'Anmelden'
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            on_release: app.on_login(*args)

        MDRaisedButton:
            text: 'Zurück'
            pos_hint: {'center_x': 0.1, 'center_y': 0.95}
            on_release: app.on_back_button()

    MDScreen:
        name: 'profile_screen'
        md_bg_color: 1, 1, 1, 1  # Weiß

        Button:
            id: sport_button
            hint_text: 'Sportart'
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            on_release: app.sport_dropdown.open(self)
           

        Button:
            id: experience_button
            text: 'Trainingserfahrung'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_release: app.duration_dropdown.open(self)

            
        Button:
            id: goals_button
            text: 'Trainingsziele'
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            on_release: app.dropdown.open(self)
           

        Button:
            id: duration_button
            hint_text: 'Trainingsdauer'
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        

        Button:
            id: frequency_button
            hint_text: 'Trainingshäufigkeit'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: app.frequency_dropdown.open(self)

        MDRaisedButton:
            text: 'Profil vervollständigen'
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            on_release: app.on_profile_complete(*args)

        MDRaisedButton:
            text: 'Zurück'
            pos_hint: {'center_x': 0.1, 'center_y': 0.95}
            on_release: app.on_back_button()



    MDScreen:
        name: 'main_menu'
        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                size_hint_y: None
                height: "48dp"

                Button:
                    text: 'Profil'
                    on_release: app.on_tab_switch('profile')

                Button:
                    text: 'Suche'
                    on_release: app.on_tab_switch('search')

                Button:
                    text: 'Matching'
                    on_release: app.on_tab_switch('matching')

                Button:
                    text: 'Nachrichten'
                    on_release: app.on_tab_switch('messages')

                Button:
                    text: 'Einstellungen'
                    on_release: app.on_tab_switch('settings')

    MDScreen:
        name: 'profile_view_screen'
        md_bg_color: 0, 0, 0, 1

        MDRaisedButton:
            text: 'Zurück'
            pos_hint: {'center_x': 0.1, 'center_y': 0.95}
            on_release: app.on_back_button()

        BoxLayout:
            orientation: 'vertical'
            padding: '32dp'
            spacing: '20dp'

            Label:
                id: profile_username
                text: 'Benutzername'
                font_size: '16sp'
                halign: 'center'
              

            Label:
                id: profile_sport
                text: 'Sportart'
                font_size: '16sp'
                halign: 'center'

            Label:
                id: profile_frequency
                text: 'Trainingshäufigkeit'
                font_size: '16sp'
                halign: 'center'

            Label:
                id: profile_duration
                text: 'Trainingsdauer'
                font_size: '16sp'
                halign: 'center'

            Label:
                id: profile_experience
                text: 'Trainingserfahrung'
                font_size: '16sp'
                halign: 'center'

            Label: 
                id: profile_goals
                text: 'Trainingsziele'
                font_size: '16sp'
                halign: 'center'

    MDScreen:
        name: 'settings_screen'
        BoxLayout:
            orientation: 'vertical'
            padding: '32dp'
            spacing: '20dp'

            Label:
                text: 'Einstellungen'
                font_size: '24sp'
                halign: 'center'

        MDRaisedButton:
            text: 'Logout'
            pos_hint: {'center_x': 0.5}
            on_release: app.on_logout()

        MDRaisedButton:
            text: 'Zurück'
            pos_hint: {'center_x': 0.1, 'center_y': 0.95}
            on_release: app.on_back_button()

'''

class MainApp(MDApp):
    current_username = None

    def build(self):
        self.setup_db()
        self.goals_dropdown = self.create_dropdown(['Fitness/Hobbysport', 'Wettkampforientiert', 'Spezifische Ziele'], 'goals_button')

        # Dropdown Menü für Trainingshäufigkeit
        self.frequency_dropdown = self.create_dropdown(['Täglich', 'Wöchentlich', 'Monatlich'], 'frequency_button')

        # Dropdown Menü für Trainingsdauer
        self.duration_dropdown = self.create_dropdown(['< 1 Stunde', '1-2 Stunden', '2+ Stunden'], 'duration_button')

        # Dropdown Menü für Trainingserfahrung
        self.experience_dropdown = self.create_dropdown(['Anfänger', 'Fortgeschritten', 'Profi'], 'experience_button')

        # Dropdown Menü für Sportart
        self.sport_dropdown = self.create_dropdown(['Laufen', 'Schwimmen', 'Fahrradfahren'], 'sport_button')
            
        return Builder.load_string(KV)
    

    def create_dropdown(self, options, button_id):
        dropdown = DropDown()
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn=btn: self.on_dropdown_select(btn.text, button_id))
            dropdown.add_widget(btn)
        return dropdown
    
    def on_dropdown_select(self, value, button_id):
        print(f"Ausgewählt: {value}")
        self.root.ids[button_id].text = value
        if button_id == 'goals_button':
            self.goals_dropdown.dismiss()
        elif button_id == 'frequency_button':
            self.frequency_dropdown.dismiss()
        elif button_id == 'duration_button':
            self.duration_dropdown.dismiss()
        elif button_id == 'experience_button':
            self.experience_dropdown.dismiss()
        elif button_id == 'sport_button':
            self.sport_dropdown.dismiss()
    
    def setup_db(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                sport TEXT,
                training_frequency TEXT,
                training_availability TEXT,
                training_duration TEXT,
                training_location TEXT,
                training_experience TEXT,
                training_goals TEXT
                
            )
        ''')
        conn.commit()
        conn.close()

    def on_dropdown_select(self, value):
        # Diese Methode wird aufgerufen, wenn eine Option aus dem Dropdown-Menü ausgewählt wird
        print(f"Ausgewählt: {value}")
        self.root.ids.goals_button.text = value


    def on_welcome_button(self, action):
        if action == 'register':
            self.root.current = 'register_screen'
        elif action == 'login':
            self.root.current = 'login_screen'

    def on_register(self, instance):
        username = self.root.ids.username_field.text
        password = self.root.ids.password_field.text

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        except sqlite3.IntegrityError:
            print(f'Der Benutzername "{username}" ist bereits vergeben.')
            return

        conn.commit()
        conn.close()

        print(f'Registriert als {username} mit Passwort {password}')
        self.current_username = username
        self.root.current = 'profile_screen'

    def on_login(self, instance):
        username = self.root.ids.login_username_field.text
        password = self.root.ids.login_password_field.text

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            # Überprüfen, ob Profilinformationen vorhanden sind.
            if user[2] and user[3] and user[4] and user[5]:  # Das sind die Indizes für die Spalten sport, training_frequency, training_duration und training_experience
                self.root.current = 'main_menu'
                self.current_username = username
            else:
                self.root.current = 'profile_screen'
                # Setzen des Benutzernamens im Registrierungsfeld, um die spätere Aktualisierung zu ermöglichen.
                self.root.ids.username_field.text = username
        else:
            print('Anmeldung fehlgeschlagen: Benutzername oder Passwort ist falsch')

    def on_profile_complete(self, instance):
        username = self.root.ids.username_field.text
        sport = self.root.ids.sport_field.text
        frequency = self.root.ids.frequency_field.text
        duration = self.root.ids.duration_field.text
        experience = self.root.ids.experience_field.text
        goals = self.root.ids.goals_field.text


        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        c.execute('UPDATE users SET sport = ?, training_frequency = ?, training_duration = ?, training_experience = ?, training_goals = ? WHERE username = ?', 
                  (sport, frequency, duration, experience, goals, username))

        conn.commit()
        conn.close()

        print(f'Profil vervollständigt für {username} mit Sportart {sport}')
        self.root.current = 'main_menu'

    def on_tab_switch(self, tab_name):
        print(f"Tab switched to: {tab_name}")
        if tab_name == 'profile':
            print("Attempting to load user profile...")
            self.load_user_profile()
        elif tab_name == 'settings':
            self.root.current = 'settings_screen'
        print(f'Tab gewechselt zu: {tab_name}')

    def load_user_profile(self):
        print("Loading user profile...")
        # Wir müssen den Benutzernamen des angemeldeten Benutzers speichern.
        username = self.current_username

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        print(f"Fetched user: {user}")

        conn.close()

        if user:
            self.root.ids.profile_username.text = f'Benutzername: {user[0]}'
            self.root.ids.profile_sport.text = f'Sportart: {user[2]}'
            self.root.ids.profile_frequency.text = f'Trainingshäufigkeit: {user[3]}'
            self.root.ids.profile_duration.text = f'Trainingsdauer: {user[4]}'
            self.root.ids.profile_experience.text = f'Trainingserfahrung: {user[5]}'
            self.root.ids.profile_goals.text = f'Trainingsziele: {user[6]}'
            self.root.current = 'profile_view_screen'
        else:
            print('Fehler beim Laden des Profils')

    def on_goals_select(self, instance, value):
        self.root.ids.goals_field.text = value

    def on_back_button(self):
        # Eine einfache Methode, um zurück zum Begrüßungsbildschirm zu navigieren.
        # Dies kann weiter angepasst werden, um zu verschiedenen Bildschirmen zurückzukehren, 
        # basierend auf der aktuellen Bildschirmposition.
        self.root.current = 'main_menu'

    def on_logout(self):
        self.current_username = None
        self.root.current = 'welcome_screen'

if __name__ == '__main__':
    MainApp().run()
