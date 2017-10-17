import os
import sys
import sqlite3

DBNAME = 'free_associate.db'
TABLENAME = 'examples'

class FreeAssociation:
    def __init__(self):
        # connect to db
        self.dbname = DBNAME
        conn = sqlite3.connect(self.dbname)
        self.c = conn.cursor()

    # 全ての単語を返します
    def all_words(self):
        sql = 'select TARGET from '+TABLENAME
        return list(set([row[0] for row in self.c.execute(sql)]))

    # 全てのキューを返します
    def all_normed_words(self):
        sql = 'select CUE from '+TABLENAME
        return list(set([row[0] for row in self.c.execute(sql)]))

    # キューとして定義されているかどうかを返します
    def is_normed(self, word):
        if word in self.all_normed_words():
            return True
        else:
            return False

    # 連想関連にある単語を返します
    def associations(self, word, step=1):
        words = []
        next_words = [word]

        for i in range(step):
            words = next_words
            next_words = []
            for word in words:
                sql = 'select TARGET from '+TABLENAME+' where CUE = "'+word+'"'
                for row in self.c.execute(sql):
                    next_words.append(row[0])
            next_words = list(set(next_words))

        return next_words

    def normed_associations(self, word, step=1):
        words = []
        next_words = [word]

        for i in range(step):
            words = next_words
            next_words = []
            for word in words:
                sql = 'select TARGET from '+TABLENAME+' where CUE = "'+word+'"'
                for row in self.c.execute(sql):
                    if self.is_normed(row[0]):
                        next_words.append(row[0])
                    else:
                        continue
            next_words = list(set(next_words))

        return next_words

    # 連想関係の強度を返します
    def cue_to_target_strength(self, cue, target):
        try:
            sql = 'select FSG from '+TABLENAME+' where CUE = "'+cue+'" and TARGET = "'+target+'"'
            res = self.c.execute(sql)
            return list(res)[0][0]
        except:
            return 0

    def indicator(self, indicator_name, cue, target):
        try:
            sql = 'select '+indicator_name+' from '+TABLENAME+' where CUE = "'+cue+'" and TARGET = "'+target+'"'
            res = self.c.execute(sql)
            return list(res)[0][0]
        except:
            return 0

    # 連想
    def mediators(self, cue, target):
        sql = 'select TARGET from '+TABLENAME+' where CUE = "'+cue+'"'
        cue_set = set([ row[0] for row in self.c.execute(sql)])
        sql = 'select CUE from '+TABLENAME+' where TARGET = "'+target+'"'
        target_set = set([ row[0] for row in self.c.execute(sql)])

        mediator_set = cue_set & target_set

        try:
            sql = 'select MSG from '+TABLENAME+' where CUE = "'+cue+'" and TARGET = "'+target+'"'
            res = self.c.execute(sql)
            MSG = list(res)[0][0]
        except:
            MSG = 0

        return list(mediator_set), MSG

    def overlaps(self, cue, target):
        sql = 'select TARGET from '+TABLENAME+' where CUE = "'+cue+'"'
        cue_set = set([ row[0] for row in self.c.execute(sql)])
        sql = 'select TARGET from '+TABLENAME+' where CUE = "'+target+'"'
        target_set = set([ row[0] for row in self.c.execute(sql)])

        overlap_set = cue_set & target_set

        try:
            sql = 'select OSG from '+TABLENAME+' where CUE = "'+cue+'" and TARGET = "'+target+'"'
            res = self.c.execute(sql)
            OSG = list(res)[0][0]
        except:
            OSG = 0

        return list(overlap_set), OSG

# EXAMPLES
if __name__=='__main__':

    fa = FreeAssociation()

    cue = 'adult'
    target = 'child'

    print('Associations of "adult"')
    print(fa.associations(cue))

    print('Association strength of "adult" and "child"')
    print(fa.cue_to_target_strength(cue, target))

    print('Mediators of "adult" and "child"')
    print(fa.mediators(cue, target))

    print('Overlaps of "adult" and "child"')
    print(fa.overlaps(cue, target))
