import time
import pandas as pd
import urllib.request as req
import json
import time

def stemp2str(data): #將自1970-01-01起之時間戳轉化為YYYY-MM-DD格式之字串，並只取2005年後數據
    ccicsv = []
    for row in data:
        # print(type(row[0]))
        if row[0] > 1104537600000: #取 2005-01 後資料
            t = time.localtime(row[0]/1000) #原資料為毫秒，需除以1000換為秒
            ts = time.strftime("%Y-%m-%d", t) #轉為字串     
            ccicsv.append([ts,row[1]])
    return ccicsv

def time2str(data):
    for i in range(len(data)):
        time_stamp = data[i]
        timestr = time_stamp.to_period("D")
        data[i] = timestr
    return data

def uscrawler(code):
    code = code.upper()
    header = {
            "Content-Type":"application/json",#; charset=UTF-8",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    urls = [ "https://sbcharts.investing.com/events_charts/us/733.json", #CPI
        "https://sbcharts.investing.com/events_charts/us/48.json", #CCI
        "https://sbcharts.investing.com/events_charts/us/300.json", #UR
        "https://sbcharts.investing.com/events_charts/us/168.json" #FFR
        ]
    # Unit 1-0 : Crawler Part : yfinance (Daily data)
    if code == "D": #in ["SP500","USD","VIX"]:
        dailydata = pd.DataFrame()#columns=["DateD","SP500","USD","VIX"]
        ii = 0
        for c,yfid in zip(["SP500","USD","VIX"],["^GSPC","DX-Y.NYB","^VIX"]):
            import yfinance as yf
            sp500 = yf.download(yfid,"2005-01-19",time.strftime('%Y-%m-%d'))
            close = sp500.iloc[:,3]
            close = close.reset_index()
            close["Date"] = time2str(close["Date"])
            for i in range(len(close.iloc[:,0])):
                close.iloc[i,0] = str(close.iloc[i,0])
            close.rename(columns={"Date":"DateD","Close":c},inplace=True)
            if ii == 0:
                dailydata = pd.merge(dailydata,close,'right',left_index=True,right_index=True)
                ii = 1 
            else:
                dailydata = pd.merge(dailydata,close,'left','DateD')
        return dailydata.round(2) #dataframe

    # Unit 1-2 : Crawler Part : Web (monthly&other)

    elif code == "M":
        monthlydata = pd.DataFrame()#columns=["DateD","SP500","USD","VIX"]
        ii = 0
        for c,url in zip(["CPI","CCI","UR"],urls[0:3]):
            resp = req.Request(url,headers=header)
            with req.urlopen(resp) as res:
                result = res.read().decode("utf-8")
            result = json.loads(result)
            data = result["data"]
            data = stemp2str(data)
            data = pd.DataFrame(data,columns=["DateM",c])
            if ii == 0:
                monthlydata = pd.merge(monthlydata,data,'right',left_index=True,right_index=True)
                ii = 1
            else:
                monthlydata = pd.concat([monthlydata,data.iloc[:,1]],1,'outer',True)
                monthlydata.fillna(method="pad",inplace=True)

        monthlydata.columns = ["DateM","CPI","CCI","UR"]
        return monthlydata.round(2)

    elif code == "OT":
        url = urls[3]
        c = 'FFR'
        resp = req.Request(url,headers=header)
        with req.urlopen(resp) as res:
            result = res.read().decode("utf-8")
        result = json.loads(result)
        data = result["data"]
        data = stemp2str(data)
        ffr = pd.DataFrame(data,columns=["dates",c])
        return ffr.round(2)     

if __name__ == '__main__':
    for code in["M","D","OT"]:
        code = code.upper()
        if code == 'M':
            monthly = uscrawler("M")
            print(monthly)
        elif code == 'D':
            daily = uscrawler('D')
            print(daily)
        elif code == 'OT':
            ffr = uscrawler("ot")
            print(ffr)