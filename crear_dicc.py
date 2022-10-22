##!/usr/bin/env python3

import string
import itertools
import argparse
import tempfile
import time
from multiprocessing import cpu_count

def crear_dicc(number_of_dicc, max_length, min_length=1):
    try:
        combinations=calc_combination(max_length, min_length)/number_of_dicc
        index=1
        x=0
        for i in range(min_length, max_length+1):
            for j in itertools.product(string.ascii_lowercase, repeat=i):
                if(x<combinations):
                    x+=1
                else:
                    index+=1
                    x=0
                password = ''.join(j)
                tempfile
                open('diccionarios/dicc_{}.txt'.format(index), 'a').write(password + '\n')
    except KeyboardInterrupt:
        print('Saliendo...')
        exit(0)

def calc_combination(max_length, min_length):
    combinations = 0
    for i in range(min_length, max_length+1):
        combinations += len(string.ascii_lowercase) ** i
    return combinations

def args_parser():
    parser = argparse.ArgumentParser(description='Script para descifrar un archivo con gpg')
    parser.add_argument('-n', '--number_of_dicc', type=int, default=cpu_count(), help='Numero de diccionarios a crear')
    parser.add_argument('-M', '--max', type=int, help='Longitud máxima de contraseña', required=True)
    parser.add_argument('-m', '--min',type=int, help='Longitud mínima de contraseña', default=1)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    starting_time = time.time()
    args = args_parser()
    print('Creando diccionarios...')
    crear_dicc(args.number_of_dicc, args.max, args.min)
    ending_time = time.time()
    print('Tiempo de ejecución: {} segundos'.format(ending_time - starting_time))