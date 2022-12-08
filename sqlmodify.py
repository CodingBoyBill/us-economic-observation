import sqlite3
import pandas as pd

def sqlmodify():
    db = sqlite3.connect('us_finance.sqlite')
    cur = db.cursor()
    data = cur.execute("""SELECT usfinanceDaily.*,usfinanceMonthly.CCI, \
                usfinanceMonthly.CPI,usfinanceMonthly.UR \
            FROM usfinanceDaily LEFT JOIN usfinanceMonthly on \
                usfinanceDaily.DateD=usfinanceMonthly.DateM;""").fetchall()
    data = pd.DataFrame(data,columns=['date','sp500','usd','vix','ffr','cci','cpi','ur'])
    data = data.interpolate()
    cur.execute("""CREATE TABLE IF NOT EXISTS \
                plot(Dates TEXT PRIMARY KEY,SP500 REAL, USD REAL, VIX REAL \
                    , FFR REAL, CCI REAL, CPI REAL,UR REAL) ;""")
    try: #若為首次輸入則使用 INSERT
        for i in range(len(data.iloc[:])):
            a = list(data.iloc[i])[:]
            cur.execute("""INSERT INTO plot \
                values('{}',{:.2f},{},{},{},{:.2f},{:.2f},{:.2f});""".format(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]))
        print('inserted!')
        db.commit()
        db.close()
    except: #非首次輸入，上方ERROR跳入下方，採UPDATE
        for i in range(len(data.iloc[:])):
            a = list(data.iloc[i])[:]
            cur.execute("""UPDATE plot SET SP500 = {:.2f}, USD = {}, VIX = {}, FFR = {}, CCI = {:.2f}, CPI = {:.2f}, \
                UR = {:.2f} WHERE Dates = '{}';""".format(a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[0]))
        print('updated!')
        db.commit()
        db.close()
if __name__ == "__main__":
    sqlmodify()