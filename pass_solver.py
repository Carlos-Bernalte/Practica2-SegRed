##!/usr/bin/env python3

import sys
import subprocess
import time
import argparse
from multiprocessing import Process, cpu_count, Value

founded = Value('i', False)

def pass_solver(i, file):
    try:
        start_time = time.time()
        with open('diccionarios/dicc_'+str(i)+'.txt', 'r') as fichero:
            for password in fichero:
                if founded.value:
                    break
                password = password.rstrip('\n')
                if(check_pass(password, file)):
                    end_time = time.time()
                    print('[Proceso {}] Clave encontrada: {}'.format(i,password))
                    open('password.txt', 'a').write('Contraseña: '+password +'\n'+calc_hora(end_time - start_time)+'\n')
                    sys.exit()
        end_time = time.time()
        print('[Proceso {}] No se encontro la contraseña. {}'.format(i, calc_hora(end_time - start_time)))
    except KeyboardInterrupt:
        print('Saliendo...')
        sys.exit()
    
def check_pass(password, file):
    try:
        # subprocess.check_output(['gpg', '--batch', '--passphrase', password, '-d', ARCHIVO, '>>', 'resultado.pdf'], stderr=subprocess.DEVNULL)
        subprocess.check_output(['gpg', '--batch', '--passphrase', password, '-d', file], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        sys.exit()
    else:
        founded.value = True
        return True

def calc_hora(segundos):
    horas = segundos // 3600
    segundos %= 3600
    minutos = segundos // 60
    segundos %= 60
    return 'Tiempo de ejecucion: '+str(int(horas))+':'+str(int(minutos))+':'+str(int(segundos))

def args_parser():
    parser = argparse.ArgumentParser(description='Script para descifrar un archivo con gpg')
    parser.add_argument('-f', '--file', type=str, help='Archivo a descifrar', required=True)
    parser.add_argument('-n', '--n_processes', type=int, default=cpu_count(), help='Numero de procesos a lanzar')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = args_parser()
    for i in range(1, args.n_processes+1):
        Process(target=pass_solver, args=(i,args.file)).start()
    





    