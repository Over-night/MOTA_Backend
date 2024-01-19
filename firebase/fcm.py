# import firebase_admin
# from firebase_admin import credentials, messaging

# cred = credentials.Certificate("private/firebase.json")
# default_app = firebase_admin.initialize_app(cred)

# def sendPush(title, msg, registrationToken, dataObject):
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=msg
#         ),
#         data=dataObject,
#         tokens=registrationToken
#     )
    
#     response = messaging.send_multicast(message)
#     print('메시지 전송 성공')