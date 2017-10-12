import os
import sys
import codecs
import glob

folder = 'type1'
input_files = glob.glob(folder+'/*.txt')

d = []

for input_file in input_files:
    f = codecs.open(input_file, 'r', 'utf-8')
    for line in f.readlines()[1:]:
        l = line.strip().split(',')
        l = [ e.strip().lower() for e in l ]
        d.append(tuple(l))

import sqlite3

dbname = 'free_associate.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

# executeメソッドでSQL文を実行する
create_table = '''create table examples (CUE, TARGET, NORMED, G int, P int, FSG num, BSG num,
                  MSG num, OSG num, M int, MMIAS int, O num, OMIAS int, QSS int, QFR int, QCON, QH, QPS, QMC num, QPR num,
                  QRSG num, QUC int, TSS int, TFR int, TCON num, TH, TPS, TMC num, TPR num, TRSG num, TUC int)'''
c.execute(create_table)

sql = '''insert into examples (CUE, TARGET, NORMED, G, P, FSG, BSG, MSG, OSG, M,
         MMIAS, O, OMIAS, QSS, QFR, QCON, QH, QPS, QMC, QPR, QRSG, QUC, TSS, TFR,
         TCON, TH, TPS, TMC, TPR, TRSG, TUC) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

for e in d:
    print(e)
    c.execute(sql, e)
conn.commit()
conn.close()
