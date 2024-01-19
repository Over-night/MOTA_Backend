from mota.models.uid_dict import UidDict

from firebase_admin import messaging, firestore
from firebase.authentication import FirebaseAuthentication

db = firestore.client()
firebase = FirebaseAuthentication()

def send_fcm_notification(user, title, body):
    try:
        user_dict = UidDict.objects.get(app=user)
        firebase_uid = user_dict.firebase.username

        dbData_ref = db.collection('fcm_token').document(firebase_uid)
        try:
            dbData_obj = dbData_ref.get()
        except:
            return None
        if not dbData_obj.exists:
            return None
        dataDict = dbData_obj.to_dict()

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=dataDict["token"]
        )
        
        res = messaging.send(message)
        
        return res
    except:
        return None
    
def load_user(request):
    authUser = firebase.getUserFromToken(request)
    try:
        dict = UidDict.objects.get(firebase=authUser)
    except:
        return None
    return dict.app