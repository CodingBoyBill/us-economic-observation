import crawler
import tosql
import sqlmodify
import plot

# 若無需重新爬取，前面的part可以註解起來，僅操作plot即可

######## Clear The  DB ########

def main():

    # tosql.clear() # 此步驟還有優化空間，tosql模組內預計可以try-except處理，就可不用每次都清掉tables

######## Get Data Part ########

    codes = ["M","D","OT"]

    for code in codes:
        data = crawler.uscrawler(code) #依序取得資料

########  To SQL Part  ########

        tosql.data2sql(data,code) #寫入資料表

######  SQL Modify Part  ######
    
    sqlmodify.sqlmodify() # 製作plot資料表，合併日月資料表並線性內插

#########  Plot Part  #########

    # num = int(input('How many lines would you want to display on your figure ? (1~2)'))
    # plot.plot(num)

if __name__ == "__main__":
    main()