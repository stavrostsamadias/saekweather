import pickle

# Ανοίγουμε το αρχείο .pkl για ανάγνωση σε λειτουργία δυαδικού ανάγνωσης ('rb')
with open('temperature_prediction_model.pkl', 'rb') as f:
    # Φορτώνουμε το μοντέλο από το αρχείο
    model = pickle.load(f)

# Εδώ μπορείτε να εξερευνήσετε το μοντέλο και να δείτε τα χαρακτηριστικά του
print(model)