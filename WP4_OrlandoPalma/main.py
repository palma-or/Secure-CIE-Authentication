import user
from server import ServerAuthority, ServerService


print("\n#####################################################")
print("\n#              Richiesta Credenziali                #")
print("\n#####################################################")

utente = user.User()
m=utente.create_message()
request=utente.request(pkwallet,salt,m) # da definire
signature=utente.sign_request(request)
serverAuth = ServerAuthority('Auth')
utente.connect(serverAuth) 
utente.send_request(request, signature)


print("\n#####################################################")
print("\n#                Richiesta Servizio                 #")
print("\n###################################################\n")

serverService=ServerService('Service')
utente.connect(serverService)
req=utente.get_request()
print(f'The server required this credentials: {req}')
credentials = utente.getfromWallet(req,utente.wuser) # da definire
utente.sendInfo(credentials)