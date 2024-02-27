import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib
import streamlit as st
import pandas as pd1
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import folium_static
import subprocess

class run_App():
    def __init__(self):
        self.run_app1()

    def run_app1(self):
        st.set_page_config(
        page_title="Πρόβλεψη Καιρικών Φαινομένων και Πυρκαγιάς",
        page_icon="fire",
        )
        # Προσθήκη κουμπιού "Περισσότερες Λειτουργίες" στην αριστερή μπάρα
        # Εμφανίζεται ένα κουμπί που όταν πατηθεί, αλλάζει τη σελίδα και μεταφέρει στη συνάρτηση step2
        # Εμφανίζεται ένα κουμπί στην αριστερή μπάρα που όταν πατηθεί, αλλάζει τη σελίδα και μεταφέρει στη συνάρτηση step2
        st.sidebar.success("Select a page above")
        data_cor = pd1.DataFrame({
            'LAT': [38.37011455642275],
            'LON': [21.429736211480577]
                                })
        st.image("https://www.saekmesol.gr/wp-content/uploads/2020/03/std_logo.png", caption="")

        # Εμφάνιση πληροφοριών κατασκευαστή και εισηγητή
        st.sidebar.title('Στοιχεία Δημιουργού')
        st.sidebar.info('Κατασκευαστής Εφαρμογής: Σταύρος Τσαμαδιάς')
        st.sidebar.info('Εισηγητής Καθηγητής: Θεοφάνης Γκαναβιάς')
        st.sidebar.info('Συμμετοχή Σ.Α.Ε.Κ. Μεσολογγίου')

        # Κεντρική περιγραφή της εφαρμογής
        st.title('Πρόβλεψη Καιρικών Φαινομένων και Πυρκαγιάς')
        st.write('Καλώς ήρθατε στην εφαρμογή πρόβλεψης καιρικών φαινομένων και πυρκαγιάς!')
        st.write('Εδώ συνδυάζουμε την προηγμένη τεχνητή νοημοσύνη με τη δύναμη των δεδομένων για να προβλέψουμε τις καιρικές συνθήκες και τον κίνδυνο πυρκαγιάς στα δάση.')

        # Προσθήκη πληροφοριών για την περιοχή και τους αισθητήρες
        st.write('Η εφαρμογή εμφανίζει αποτελέσματα μόνο για την περιοχή του Μεσολογγίου.')
        st.write('Τα δεδομένα προέρχονται από αισθητήρες που εγκαθίστανται στο Μεσολόγγι, συμπεριλαμβανομένων των:')
        st.write('- Ανεμόμετρο Αισθητήρας Ταχύτητας Ανέμου')
        st.write('- DFRobot I2C Αισθητήρας Υγρασίας & Θερμοκρασίας (Stainless Steel Shell)')
        st.write('- Gravity Αναλογικός Αισθητήρας CO2 - MG-811')

        # Εμφάνιση χάρτη Μεσολογγίου
        st.write('Ο χάρτης του Μεσολογγίου:')
        st.map(data_cor, zoom=16)

        #-----------------------------
        # Διάβασμα του αρχείου Excel
        # Διάβασμα των δεδομένων από το Excel
        df = pd1.read_excel("weather_data.xlsx")

        # Δημιουργία του χάρτη
        st.subheader("Χάρτης με τις θέσεις των παρατηρήσεων")

        # Αρχικοποίηση του χάρτη
        m = folium.Map(location=[38.3701, 21.4297], zoom_start=10)

        # Προσθήκη σημείων στο χάρτη
        for index, row in df.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']], popup=row['weather_now']).add_to(m)

        # Εμφάνιση του χάρτη
        folium_static(m)
        #------------------------------------------------------------------

        # Διαβάζουμε τα δεδομένα από το Excel
        data = pd1.read_excel('weather_data.xlsx')

        # Ορίζουμε τον τίτλο και την περιγραφή της σελίδας
        st.title("Πρόγνωση καιρού για το Μεσολόγγι")
        st.write("Αυτή η εφαρμογή παρέχει πληροφορίες για τον καιρό στην πόλη του Μεσολογγίου.")

        # Εμφάνιση της τρέχουσας θερμοκρασίας
        current_temperature = data['Temperature'].iloc[-1]
        st.write(f"Η τρέχουσα θερμοκρασία είναι: {current_temperature} °C")

        # Εμφάνιση του γραφήματος με την πορεία της θερμοκρασίας
        st.write("## Πορεία Θερμοκρασίας")
        st.line_chart(data['Temperature'])

        # Εμφάνιση του γραφήματος με την υγρασία
        st.write("## Υγρασία")
        st.line_chart(data['Humidity'])

        # Εμφάνιση του γραφήματος με την ταχύτητα του ανέμου
        st.write("## Ταχύτητα Ανέμου")
        st.line_chart(data['Wind'])

        # Εμφάνιση του χάρτη με την τοποθεσία του Μεσολογγίου
        st.write("## Τοποθεσία Μεσολογγίου")
        st.write("Γεωγραφικό Πλάτος: 38.3701")
        st.write("Γεωγραφικό Μήκος: 21.4297")

        # Προαιρετική εμφάνιση δεδομένων από το Excel
        #if st.checkbox("Προβολή δεδομένων από το Excel"):
        #    st.write("## Δεδομένα από το Excel")
        #    st.write(data)

        fig = px.scatter_mapbox(data, lat='latitude', lon='longitude', color='Temperature',
                        hover_data=['Temperature', 'Humidity', 'Dew_Point', 'Wind'],
                        zoom=10, height=600)
        # Ορισμός του είδους του χάρτη
        fig.update_layout(mapbox_style="open-street-map")

        # Εμφάνιση του χάρτη με το Streamlit
        st.plotly_chart(fig)
        st.write("Ο χάρτης είναι διαδραστικός και παρέχει πληροφορίες όπως η θερμοκρασία, η υγρασία, το σημείο δρόσου και η ταχύτητα του ανέμου όταν κάνετε hover πάνω από κάθε σημείο")
        #-----------------------------------------------------------------

        # Διαβάζετε τα δεδομένα από το αρχείο Excel
        data = pd1.read_excel('weather_data.xlsx')

        # Πεδίο επιλογής για την προβολή των δεδομένων
        show_data = st.checkbox("Εμφάνιση Δεδομένων από το Excel")

        # Εάν το πεδίο επιλογής είναι τσεκαρισμένο, εμφανίστε τα δεδομένα
        if show_data:
            st.write("Δεδομένα από το Excel:")
            st.write(data)
        # Περιγραφή της αρχικής σελίδας
        st.sidebar.subheader("Αρχική Σελίδα")
        st.sidebar.write("Καλώς ήρθατε στην εφαρμογή πρόβλεψης καιρικών συνθηκών!")
        st.sidebar.write("Σκοπός της εφαρμογής είναι να παρέχει πληροφορίες σχετικά με τις καιρικές συνθήκες και την πιθανότητα πυρκαγιάς.")
        st.sidebar.write("Μπορείτε να επιλέξετε το είδος του γραφήματος που θέλετε να δείτε από το μενού στα αριστερά.")

        # Κουμπί για μετάβαση στα γραφήματα
        #if st.sidebar.button("Δείτε τα Γραφήματα"):
        #    st.sidebar.success("Μετάβαση στα Γραφήματα!")

        # Αριστερό μέρος με περιγραφή των γραφημάτων
        st.sidebar.subheader("Πληροφορίες για τα Γραφήματα")
        st.sidebar.write("Τα γραφήματα παρουσιάζουν διάφορες πληροφορίες σχετικά με τις καιρικές συνθήκες και την πιθανότητα πυρκαγιάς.")
        st.sidebar.write("Μπορείτε να επιλέξετε το είδος του γραφήματος από το μενού 'Επιλογή Γραφήματος'.")
        st.sidebar.write("Για περισσότερες πληροφορίες σχετικά με κάθε γράφημα, κάντε κλικ στον τίτλο του γραφήματος.")
        #-------------------------------------------------------------------------------------------


        #---------------------------------------------------------------------------------------------------
        # Διαβάστε τα δεδομένα από το αρχείο Excel
        data = pd1.read_excel('weather_data.xlsx')

        # Λίστα με τα διαθέσιμα είδη γραφημάτων
        available_charts = [
                'Σύγκριση πραγματικών και προβλεπόμενων καιρικών συνθηκών',
                'Διάγραμμα πυκνότητας προβλεπόμενων καιρικών συνθηκών',
                'Κατανομή προβλεπόμενων καιρικών συνθηκών',
                'Διάγραμμα πυκνότητας FWI',
                'Διάγραμμα πυκνότητας θερμοκρασίας',
                'Πρόβλεψη Πυρκαγιάς'
        ]

        # Επιλογή γραφήματος από τον χρήστη
        selected_chart = st.selectbox("Επιλέξτε το είδος του γραφήματος", available_charts)

        # Χωρισμός των δεδομένων σε χαρακτηριστικά και ετικέτες
        X = data[['fwi_value', 'Temperature', 'Humidity', 'Wind', 'rain']].values
        y = data['weather_now'].values

        # Κωδικοποίηση των κατηγορικών ετικετών σε αριθμητικές τιμές
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        # Χωρισμός των δεδομένων σε σετ εκπαίδευσης και ελέγχου
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Εκπαίδευση του νευρωνικού δικτύου
        model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
        model.fit(X_train, y_train)

        # Πρόβλεψη των καιρικών συνθηκών για τα δεδομένα ελέγχου
        y_pred = model.predict(X_test)

        # Υπολογισμός της ακρίβειας του μοντέλου
        accuracy = accuracy_score(y_test, y_pred)


        # Ανάλογα με την επιλογή του χρήστη, προβάλλουμε το αντίστοιχο γράφημα
        if selected_chart == available_charts[0]:  # Σύγκριση πραγματικών και προβλεπόμενων καιρικών συνθηκών
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Σύγκριση πραγματικών και προβλεπόμενων καιρικών συνθηκών'")
            st.sidebar.write("Σύγκριση πραγματικών και προβλεπόμενων καιρικών συνθηκών")
            st.sidebar.write("Στο γράφημα αυτό, εμφανίζεται μια διασπορά των πραγματικών και προβλεπόμενων καιρικών συνθηκών.")
            st.sidebar.write("Ο άξονας X αντιπροσωπεύει τις πραγματικές καιρικές συνθήκες, ενώ ο άξονας Y αντιπροσωπεύει τις προβλεπόμενες καιρικές συνθήκες.")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(y_test, y_pred, alpha=0.5)
            ax.set_xlabel('Πραγματικές Καιρικές Συνθήκες')
            ax.set_ylabel('Προβλεπόμενες Καιρικές Συνθήκες')
            ax.set_title('Σύγκριση Πραγματικών και Προβλεπόμενων Καιρικών Συνθηκών')
            ax.set_xticks(np.arange(3))
            ax.set_xticklabels(['Sunny', 'Cloudy', 'Rainy'])
            ax.set_yticks(np.arange(3))
            ax.set_yticklabels(['Sunny', 'Cloudy', 'Rainy'])
            ax.grid(True)
            st.pyplot(fig)
        elif selected_chart == available_charts[1]:  # Διάγραμμα πυκνότητας προβλεπόμενων καιρικών συνθηκών
            st.write("Διάγραμμα πυκνότητας προβλεπόμενων καιρικών συνθηκών")
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Διάγραμμα πυκνότητας προβλεπόμενων καιρικών συνθηκών'")
            st.sidebar.write("Διάγραμμα πυκνότητας προβλεπόμενων καιρικών συνθηκών")
            st.sidebar.write("Στο γράφημα αυτό, εμφανίζεται η κατανομή των προβλεπόμενων καιρικών συνθηκών σε σχέση με τη συχνότητά τους.")
            st.sidebar.write("Ο άξονας X αντιπροσωπεύει τις προβλεπόμενες καιρικές συνθήκες.")
            st.sidebar.write("Ο άξονας Y αντιπροσωπεύει τη συχνότητα της κάθε κατηγορίας.")
            fig, ax = plt.subplots()
            ax.hist(y_pred, bins=10, color='blue', alpha=0.7)
            ax.set_xlabel('Προβλεπόμενες Καιρικές Συνθήκες')
            ax.set_ylabel('Συχνότητα')
            st.pyplot(fig)
        elif selected_chart == available_charts[2]:  # Κατανομή προβλεπόμενων καιρικών συνθηκών
            st.write("Κατανομή προβλεπόμενων καιρικών συνθηκών")
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Κατανομή προβλεπόμενων καιρικών συνθηκών'")
            st.sidebar.write("Κατανομή προβλεπόμενων καιρικών συνθηκών")
            st.sidebar.write("Στο γράφημα αυτό, εμφανίζεται η κατανομή των προβλεπόμενων καιρικών συνθηκών.")
            st.sidebar.write("Ο άξονας X αντιπροσωπεύει τις προβλεπόμενες καιρικές συνθήκες.")
            st.sidebar.write("Ο άξονας Y αντιπροσωπεύει τη συχνότητα της κάθε κατηγορίας.")
            fig, ax = plt.subplots()
            sns.histplot(y_pred, kde=True, ax=ax)
            st.pyplot(fig)
        elif selected_chart == available_charts[3]:  # Διάγραμμα πυκνότητας FWI
            st.write("Διάγραμμα πυκνότητας FWI")
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Διάγραμμα πυκνότητας FWI'")
            st.sidebar.write("Διάγραμμα πυκνότητας FWI")
            st.sidebar.write("Στο γράφημα αυτό, εμφανίζεται η κατανομή του FWI (Fire Weather Index).")
            st.sidebar.write("Ο άξονας X αντιπροσωπεύει την τιμή του FWI.")
            st.sidebar.write("Ο άξονας Y αντιπροσωπεύει τη συχνότητα των τιμών.")
            fig, ax = plt.subplots()
            sns.histplot(data['fwi_value'], kde=True, ax=ax)
            st.pyplot(fig)
        elif selected_chart == available_charts[4]:  # Διάγραμμα πυκνότητας θερμοκρασίας
            st.write("Διάγραμμα πυκνότητας θερμοκρασίας")
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Διάγραμμα πυκνότητας θερμοκρασίας'")
            st.sidebar.write("Διάγραμμα πυκνότητας θερμοκρασίας")
            st.sidebar.write("Στο γράφημα αυτό, εμφανίζεται η κατανομή της θερμοκρασίας.")
            st.sidebar.write("Ο άξονας X αντιπροσωπεύει την τιμή της θερμοκρασίας.")
            st.sidebar.write("Ο άξονας Y αντιπροσωπεύει τη συχνότητα των τιμών.")
            fig, ax = plt.subplots()
            sns.histplot(data['Temperature'], kde=True, ax=ax)
            st.pyplot(fig)
        elif selected_chart == available_charts[5]:  # Πρόβλεψη Πυρκαγιάς
            st.write("Πρόβλεψη Πυρκαγιάς")
            st.sidebar.subheader("Πληροφορίες για το γράφημα 'Πρόβλεψη Πυρκαγιάς'")
            st.sidebar.write("Πρόβλεψη Πυρκαγιάς")
            st.sidebar.write("Το γράφημα αυτό παρουσιάζει την πρόβλεψη πιθανότητας πυρκαγιάς για τα δεδομένα ελέγχου.")
            st.sidebar.write("Χρησιμοποιείται ένας αλγόριθμος κατηγοριοποίησης για να κατατάξει την πιθανότητα σε χαμηλό, μέτριο ή υψηλό κίνδυνο πυρκαγιάς, ανάλογα με το κατώφλι πιθανότητας που ορίζεται.")
            st.sidebar.write("Χρησιμοποιήθηκαν τρία κατώφλια πιθανότητας: 0.3, 0.5 και 0.7.")
            # Πρόβλεψη της πιθανότητας πυρκαγιάς

            fire_prediction = model.predict_proba(X_test)[:, 1]

            # Ορισμός των κατωφλιών πιθανότητας για την πυρκαγιά
            fire_thresholds = [0.3, 0.5, 0.7]

            # Κατηγορίες πυρκαγιάς
            fire_categories = ['Low', 'Moderate', 'High']

            # Υπολογισμός των ετικετών πυρκαγιάς για κάθε κατώφλι πιθανότητας
            fire_labels = [fire_categories[np.argmax(fire_prediction_row >= threshold)] for fire_prediction_row in
                           fire_prediction for threshold in fire_thresholds]

            fire_colors = ['green', 'yellow', 'orange', 'red']
            fig, ax = plt.subplots()
            sns.histplot(fire_prediction, kde=True, ax=ax)
            for threshold, label, color in zip(fire_thresholds, fire_labels, fire_colors):
                plt.axvline(x=threshold, color=color, linestyle='--', label=label)
            plt.legend(title='Fire Risk')
            st.pyplot(fig)

            # Αποθηκεύστε το μοντέλο
            joblib.dump(model, 'weather_prediction_model.joblib')


    def run_data():
        subprocess.run(["python", "databasestreamlit.py"])  # Εκτέλεση του page1.py



if __name__=="__main__":
    app = run_App()
run_App.run_data()
