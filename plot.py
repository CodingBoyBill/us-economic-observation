import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def plot(num):
    db = sqlite3.connect('us_finance.sqlite')
    cur = db.cursor()
    data = cur.execute("""SELECT * FROM plot""").fetchall()
    db.close()
    data = pd.DataFrame(data,columns=['DATE','SP500','USD','VIX','FFR','CCI','CPI','UR'])

    if num == 1:
        code = input("Which index would you want to plot ? ")
        code = code.upper()
        plt.figure(figsize=(16,8))
        plt.plot(data['DATE'],data[code],color='r',label=code)
        plt.legend()
        plt.xlabel('year',fontsize=16)
        plt.xticks([250*i for i in range(-1,19,1)],[2004+i for i in range(20)])
        plt.ylabel(code,fontsize=16)
        plt.title(code,fontsize=22)
        plt.show()
    if num == 2:
        code1 = input("Input first index . ").upper()
        code2 = input("Input second index . ").upper()
        fig, ax = plt.subplots(figsize=(16,8))
        ax.plot(data['DATE'],data[code1],color='r',label=code1,linewidth=1) 
        ax.set_ylabel(code1,fontsize=16)
        ax.tick_params(axis='y')
        ax2 = ax.twinx()
        ax2.plot(data['DATE'],data[code2],color='g',label=code2,linewidth=1)
        ax2.set_ylabel(code2,fontsize=16)
        ax2.tick_params(axis='y')
        fig.legend(loc=2, bbox_to_anchor=(0,1), bbox_transform=ax2.transAxes)
        plt.xticks([250*i for i in range(-1,19,1)],[2004+i for i in range(20)])
        plt.title(code1 + " & " + code2 + " compare ",fontsize=22)
        plt.show()

if __name__ == "__main__":
    plot(2)
            
