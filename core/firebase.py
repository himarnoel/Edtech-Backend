import firebase_admin
import os
from firebase_admin import credentials

cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
firebase_admin.initialize_app(cred)
