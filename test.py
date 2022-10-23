'''Descifrar la contraseña de un archivo con gpg con letras en minúsculas'''

import sys
import subprocess
import time
import itertools
import string
CHARS = string.ascii_lowercase

def main():
    try:
        start_time = time.time()
        for i in range(1, 5):
            for password in itertools.product(CHARS, repeat=i):
                password = ''.join(password)
                if(check_pass(password)):
                    end_time = time.time()
                    total_time = end_time - start_time
                    print('La clave es: {}'.format(password))
                    sys.exit()
    except KeyboardInterrupt:
        print('Saliendo...')
        sys.exit()

def check_pass(password):
    try:
        subprocess.check_output(['gpg', '--batch', '--passphrase', password, '-d', 'archivo.gpg'], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        sys.exit()
    else:
        return True
