# coustruct splite db for FreeAssociation
import os
import sys
import codecs
import glob
# for using sqlite
import sqlite3

# folder in which source data exist
folder = 'source'
input_files = glob.glob(folder+'/*.txt')

# store the source data temporally with tuple form
d = []
for input_file in input_files:
    f = codecs.open(input_file, 'r', 'utf-8')
    for line in f.readlines()[1:]:
        l = line.strip().split(',')
        l = [ e.strip().lower() for e in l ]
        d.append(tuple(l))

# connect to sqlite database
dbname = 'free_associate.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()

# activate sql with execute method
# create table
create_table = '''create table examples (CUE, TARGET, NORMED, G int, P int, FSG num, BSG num,
                  MSG num, OSG num, M int, MMIAS int, O num, OMIAS int, QSS int, QFR int, QCON, QH, QPS, QMC num, QPR num,
                  QRSG num, QUC int, TSS int, TFR int, TCON num, TH, TPS, TMC num, TPR num, TRSG num, TUC int)'''
c.execute(create_table)

# store the data to the sqlite database
sql = '''insert into examples (CUE, TARGET, NORMED, G, P, FSG, BSG, MSG, OSG, M,
         MMIAS, O, OMIAS, QSS, QFR, QCON, QH, QPS, QMC, QPR, QRSG, QUC, TSS, TFR,
         TCON, TH, TPS, TMC, TPR, TRSG, TUC) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
c.executemany(sql, d)

conn.commit()
# disconnect to the sqlite database
conn.close()
