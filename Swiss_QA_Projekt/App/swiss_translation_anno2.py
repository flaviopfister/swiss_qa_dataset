import streamlit as st
import pandas as pd
import random
import csv
from datetime import datetime

# Page Config
st.set_page_config(page_title="Schweiz Fragen und Antworten")

# Lade die Fragen aus dem CSV - Hier den Dateinamen und das Trennzeichen anpassen
questions_df = pd.read_csv("qald_9_plus_dbpedia_de.csv", sep=";")
# Set ID as index
questions_df.set_index("internal ID", inplace=True)


####### FUNKTIONEN ########

# Funtkion, welche die ersten 10 IDs aus der Liste holt und diese aus der Liste löscht
def fist10ID(file_path):
    # Liste für die ersten 10 Zahlen
    first_10_id= []

    # Öffnen und Lesen der Datei
    with open(file_path, 'r') as file:
        # Lesen aller Zeilen aus der Datei
        lines = file.readlines()

        # Extrahieren der ersten 10 Zahlen und Hinzufügen zur Liste
        for line in lines[:10]:
            number = int(line.strip())
            first_10_id.append(number)

    # Löschen der ersten 10 Zeilen aus der ursprünglichen Datei
    with open(file_path, 'w') as file:
        file.writelines(lines[10:])

    return first_10_id



# Funktion, die 10 zufällige IDs und Fragen zurückgibt

def get_random_questions(num_questions):
    ids = []
    questions = []
    for _ in range(num_questions):
        id = random.randint(0, len(missingID))
        question = questions_df.loc[missingID[id], "Frage"]
        ids.append(missingID[id])
        questions.append(question)
    return ids


# Funktion zum Speichern der Antwort
def save_answer(question_id, user_answer, number):
    if user_answer:
        # Erstelle einen eindeutigen Dateinamen mit Datum und Uhrzeit
        timestamp = st.session_state.timestamp
        filename = f"Answers/antworten_{timestamp}.csv"

        # Schreibe die Antwort in die CSV-Datei
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([question_id, user_answer, st.session_state.dialekt])

        st.success("Antwort wurde gespeichert!")
        if number == 9:
            st.balloons()
            st.subheader("Vielen Dank für deine Teilnahme! Falls du noch weiter Lust hast, kannst du die Page neu laden und weitere Fragen übersetzen.")
        

def display_question(id,number, questions_df):
    form_key = f"form_{number}"
    with st.form(form_key, clear_on_submit=False):

        st.write(f"Frage ID: {id[number]}")
        st.write(questions_df.loc[id[number], "Frage"])
        user_answer = st.text_input("Ihre Übersetzung ins Schweizerdeutsch 🇨🇭")

        submit = st.form_submit_button('Antwort speichern')
        if submit:
            save_answer(id[number], user_answer, number)


# Starte die App
if __name__ == "__main__":

    st.title("🇨🇭 Annotations-Tool für Schweizerdeutsch 🇨🇭")
    st.write("In diesem Tool können deutsche Fragen von Ihnen ins Schweizerdeutsche übersetzt werden. So wird ein schweizerdeutscher Datensatz aufgebaut, der für NLP / QA-Tasks genutzt werden kann.")
    st.write("ACHTUNG: Es geht nicht darum die Fragen zu beantworten, sondern sie zu übersetzen.")
    
    # Session State
    if 'random_questions' not in st.session_state:
        st.session_state.random_questions = []
        st.session_state.random_questions = fist10ID('missingID.txt')

    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    
    if  len(st.session_state.random_questions) == 0:
        st.header('Alle Fragen wurden übersetzt. Vielen Dank für deine Teilnahme!')
    
    else:     
        st.header("Für eine sinnvolle Übersetzung, wähle bitte zuerst deinen Dialekt aus.")
        # Formular für die Auswahl des Dialekts
        form_key = "dialekt_form"
        if 'dialekt' not in st.session_state:
            st.session_state.dialekt = ''
        with st.form(key=form_key, clear_on_submit=False):
            option = st.selectbox('Welcher Region würdest du deinen Dialekt zuordnen?',
                                    ('Basel', 'Bern', 'Graubünden', 'Zentralschweiz', 'Ostschweiz', 'Wallis', 'Zürich'), index = None, placeholder="Wähle deinen Dialekt")
            submit = st.form_submit_button('Auswahl speichern')
            if submit:
                # Aktualisiere die Sitzungsvariable
                st.session_state.dialekt = option
                st.success("Auswahl wurde gespeichert!")

        st.header("Übersetze die folgenden Fragen ins Schweizerdeutsche 🇨🇭")
        st.write("Ein kleiner Tipp: Schribe die Frage so, wie du sie in einer SMS / WhatsApp-Nachricht schreiben würderst.")
        # Anzeige der zu Annotation ausgewählten Fragen
        display_question(st.session_state.random_questions, 0, questions_df)
        display_question(st.session_state.random_questions, 1, questions_df)
        display_question(st.session_state.random_questions, 2, questions_df)
        display_question(st.session_state.random_questions, 3, questions_df)
        display_question(st.session_state.random_questions, 4, questions_df)
        display_question(st.session_state.random_questions, 5, questions_df)
        display_question(st.session_state.random_questions, 6, questions_df)
        display_question(st.session_state.random_questions, 7, questions_df)
        display_question(st.session_state.random_questions, 8, questions_df)
        display_question(st.session_state.random_questions, 9, questions_df)


# start: streamlit run swiss_translation_anno2.py        