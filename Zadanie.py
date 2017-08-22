#!/usr/bin/env python3.6

import csv
import time

list_of_records = [[0], [0], [0]] #lista wartosci z akcelerometrow w 3 wymiarach
minimal_value_of_movement = 1 #minimalna roznica wychylenia w dowolnej płaszczyznie - roboczo przyjelam jako 1
move_track = dict() #slownik zawierajacy poczatek interwalu 30 sekundowego - klucz oraz opis czy ruch nastapil czy nie
                    #  - wartosc

'''
Pozwolilam sobie przyjac, ze plik pozbawiony jest artefaktow oraz innych wartosci blednych.
'''
with open('acc_data.csv', newline='') as csvfile:
    start_time = time.mktime(time.strptime(next(csvfile).split(',')[0][:-4], "%Y-%m-%d %H:%M:%S"))
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        time_stamp = time.mktime(time.strptime(row[0][:-4], "%Y-%m-%d %H:%M:%S"))
        if time_stamp > start_time +30:
            #ruch okreslany jest jako roznica pomiedzy maksymalnym i minimalnym odczytem w danej osi
            movement = [max(list_of_records[0])-min(list_of_records[0]),
                        max(list_of_records[1])-min(list_of_records[1]),
                        max(list_of_records[2])-min(list_of_records[2])]
            if any(i > minimal_value_of_movement for i in movement):
                move_track[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))] = 'ruch'
            else:
                move_track[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))] = 'brak ruchu'
            list_of_records = []
            start_time = time_stamp
        else:
            list_of_records.append([float(row[3]), float(row[5]), float(row[7])])

for move in move_track:
    print(move, move_track[move])
