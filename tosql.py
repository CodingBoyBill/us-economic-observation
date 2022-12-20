import sqlite3
import crawler
import pandas as pd
def clear():
    db = sqlite3.connect("us_finance.sqlite")
    cur = db.cursor()
    cur.execute("""DROP TABLE usfinanceDaily""")
    cur.execute("""DROP TABLE usfinanceMonthly""")
    db.commit()
    db.close()

def data2sql(data,code):
    code = code.upper()
    print(data)
    db = sqlite3.connect("us_finance.sqlite")
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS usfinanceDaily \
                   (DateD TEXT PRIMARY KEY, SP500 REAL, USD REAL, VIX REAL) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS usfinanceMonthly \
                   (Indexx INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                    DateM TEXT, CPI REAL, CCI REAL, UR REAL) """)
    if code == 'D':
        print(' updating daily data.... ')
        data.to_sql('usfinanceDaily', db, if_exists='replace', index=False)
        db.close()
    elif code == 'M':
        print(' updating monthly data.... ')
        data.to_sql('usfinanceMonthly', db, if_exists='replace', index=False)
        db.close()

    elif code == "OT":
        print(' updating other data.... ')
        data.to_sql('FFR', db, if_exists='replace', index=False)
        db.close()

if __name__ == "__main__":
    code = 'OT'
    data = crawler.uscrawler(code)
    print(data)
    data2sql(data,code)
