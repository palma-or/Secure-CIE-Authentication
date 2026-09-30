import subprocess
class CIE:
    def sign(pin, data):
        if pin == '0000':
            fp = open('request.txt','w')
            fp.write(str(data))
            fp.close()
            subprocess.run(['openssl', 'dgst', '-sha256', '-sign', './User/user_key.pem', '-out', 'signature.bin', 'request.txt'])
            fp = open('signature.bin','rb')
            signature = fp.read()
            fp.close()
            print("Richiesta firmata")
            return signature
        else:
            print("Pin errato")
            exit(0)