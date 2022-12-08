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
                   (DateD TEXT PRIMARY KEY, SP500 REAL, USD REAL, VIX REAL, FR REAL) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS usfinanceMonthly \
                   (Indexx INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                    DateM TEXT, CPI REAL, CCI REAL, UR REAL) """)
    if code == 'SP500':
        data.to_sql('usfinanceDaily', db, if_exists='append', index=False)
        db.close()
    elif code == 'CPI':
        data.to_sql('usfinanceMonthly', db, if_exists='append', index=False)
        db.close()
    elif code in ['CCI','UR']:
        for row,index in zip(data.iloc[:,1],[i for i in range(1,len(data.iloc[:,1])+1)]):
            cur.execute(f"""UPDATE usfinanceMonthly SET {code} = {row} WHERE Indexx = {index}""")
            print(f"""UPDATE usfinanceMonthly SET {code} = {row} WHERE Indexx = {index}""")
        db.commit()
        db.close()

    elif code in ['USD','VIX','FR']:
        for row,index in zip(data.iloc[:,1],data.iloc[:,0]):
            cur.execute(f"""UPDATE usfinanceDaily SET {code} = {row} WHERE DateD = '{index}'""")
            print(f"""UPDATE usfinanceDaily SET {code} = {row} WHERE DateD = '{index}'""")
        db.commit()    
        if code == "FR":
            fill = cur.execute('''SELECT DateD,FR FROM usfinanceDaily''').fetchall()
            fill = pd.DataFrame(fill,columns=['DateD','FR'])
            fill.fillna(method='pad',inplace=True)
            fill.fillna(method='bfill',inplace=True)
            for row,index in zip(fill.iloc[:,1],fill.iloc[:,0]):
                print(f"""UPDATE usfinanceDaily SET {code} = {row} WHERE DateD = '{index}'""")
                cur.execute(f"""UPDATE usfinanceDaily SET {code} = {row} WHERE DateD = '{index}'""")
        db.commit()
        db.close()

if __name__ == "__main__":
    code = 'fr'
    data = crawler.uscrawler(code)
    data2sql(data,code)
