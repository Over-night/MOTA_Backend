# import os, environ, json
# from pathlib import Path
# import base64

# BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env(DEBUG=(bool, True))
# environ.Env.read_env(
#     env_file=os.path.join(BASE_DIR, '.env')
# )

# FIREBASE_JSON = {
#     "type": env('TYPE'),
#     "project_id": env('PROJECT_ID'),
#     "private_key_id": env('PRIVATE_KEY_ID'),
#     "private_key": env('PRIVATE_KEY').replace('\\n', '\n'),
#     "client_email": env('CLIENT_EMAIL'),
#     "client_id": env('CLIENT_ID'),
#     "auth_uri": env('AUTH_URI'),
#     "token_uri": env('TOKEN_URI'),
#     "auth_provider_x509_cert_url": env('AUTH_PROVIDER_X509_CERT_URL'),
#     "client_x509_cert_url": env('CLIENT_X509_CERT_URL'),
#     "universe_domain": env('UNIVERSE_DOMAIN')
# }


# # FIREBASE_JSON = json.dumps(dicts)
# # print(FIREBASE_JSON)

# # def get_firebase_json():
# #     return FIREBASE_JSON