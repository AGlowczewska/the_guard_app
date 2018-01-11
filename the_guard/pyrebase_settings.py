import pyrebase

config = {
    'apiKey': 'AIzaSyCHL_Er9JtpQbadJtoaZbvYusIY-tBRVC0',
    'authDomain': 'guardapp-ac65a.firebaseapp.com',
    'databaseURL': 'https://guardapp-ac65a.firebaseio.com',
    'projectId': 'guardapp-ac65a',
    'storageBucket': 'guardapp-ac65a.appspot.com',
    'messagingSenderId': '299985780377'
}

# initialize app with config
firebase = pyrebase.initialize_app(config)

# authenticate a user
auth = firebase.auth()

db = firebase.database()
