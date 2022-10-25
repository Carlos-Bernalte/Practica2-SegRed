##!/usr/bin/env python3

import sys
import subprocess
import time
import argparse
import string
import itertools
import os
import shutil

from multiprocessing import Process, cpu_count, Value

founded = Value('i', False)
DIR='diccionarios/'
processes = []

def crear_dicc(n_processes, max_length, min_length=1):

    combinations=calc_combinations(max_length, min_length)//n_processes
    index=1
    x=1
    for i in range(min_length, max_length+1):
        for j in itertools.product(string.ascii_lowercase, repeat=i):
            
            password = ''.join(j)
            open('{}dicc_{}.txt'.format(DIR,index), 'a').write(password + '\n')
            if(x>=combinations and index<n_processes):
                index+=1
                x=1
            else:
                x+=1

def calc_combinations(max_length, min_length):
    combinations = 0
    for i in range(min_length, max_length+1):
        combinations += len(string.ascii_lowercase) ** i
    return combinations

def pass_solver(i, file):
    try:
        start_time = time.time()
        with open('{}dicc_{}.txt'.format(DIR,i), 'r') as fichero:
            for password in fichero:
                if founded.value:
                    break
                password = password.rstrip('\n')
                if(check_pass(password, file)):
                    end_time = time.time()
                    print('[Proceso {}] Clave encontrada: {}'.format(i,password))
                    open('password.txt', 'a').write('clave: '+password +'\n'+'Tiempo de ejecución: '+calc_hora(end_time - start_time)+'\n')
                    sys.exit()
        end_time = time.time()
        print('[Proceso {}] No se encontró la clave. {}'.format(i, calc_hora(end_time - start_time)))
    except KeyboardInterrupt:
        print('[Proceso {}] Se ha interrumpido el proceso'.format(i))
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
    return str(int(horas))+':'+str(int(minutos))+':'+str(int(segundos))

def args_parser():
    parser = argparse.ArgumentParser(description='Script para descifrar un archivo con gpg')
    parser.add_argument('-f', '--file', type=str, help='Archivo a descifrar', required=True)
    parser.add_argument('-n', '--n_processes', type=int, default=cpu_count(), help='Numero de procesos a lanzar')
    parser.add_argument('-m', '--min',type=int, help='Longitud mínima de clave', default=1)
    parser.add_argument('-M', '--max', type=int, help='Longitud máxima de clave', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__': 
    try:
        args = args_parser()

        # Crear directorio y los diccionarios
        starting_time = time.time()
        if os.path.exists(DIR):
            shutil.rmtree(DIR)
        os.mkdir(DIR)
        print('Creando diccionarios...')
        crear_dicc(args.n_processes, args.max, args.min)
        ending_time = time.time()
        print('Diccionarios creados en {} segundos. Total de combinaciones: {}'.format(calc_hora(ending_time - starting_time), calc_combinations(args.max, args.min)))
        
        # Lanzar los procesos para resolver el archivo
        print('Iniciando procesos...')
        for i in range(1, args.n_processes+1):
            p = Process(target=pass_solver, args=(i, args.file))
            p.start()
            processes.append(p)
    
        print('Procesos iniciados, buscando clave. Presione Ctrl+C para interrumpir el proceso')

        for p in processes:
            p.join()
        

    except KeyboardInterrupt:
        if os.path.exists(DIR):
            shutil.rmtree(DIR)
        print('Saliendo...')
        exit(0)