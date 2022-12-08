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
    url = [ "https://sbcharts.investing.com/events_charts/us/48.json", #CCI
        "https://sbcharts.investing.com/events_charts/us/733.json", #CPI
        "https://sbcharts.investing.com/events_charts/us/168.json", #FFR
        "https://sbcharts.investing.com/events_charts/us/300.json" #UR
        ]
    # Unit 1-0 : Crawler Part : yfinance
    if code in ["SP500","USD","VIX"]:
        if code == "SP500": yfid="^GSPC"
        elif code == "USD": yfid="DX-Y.NYB"
        elif code == "VIX": yfid="^VIX"

        import yfinance as yf
        sp500 = yf.download(yfid,"2005-01-19",time.strftime('%Y-%m-%d'))
        close = sp500.iloc[:,3]
        close = close.reset_index()
        close["Date"] = time2str(close["Date"])
        for i in range(len(close.iloc[:,0])):
            close.iloc[i,0] = str(close.iloc[i,0])
        close.rename(columns={"Date":"DateD","Close":code},inplace=True)
        return close #dataframe
        
    # Unit 1-1 : Crawler Part : JSON API    
    
    elif code in ['USD',"VIX"]:
        with open(code+".json") as f:
            get = json.load(f)
            get = get["data"]
        data = []
        for i in range(len(get)):
            get[i][0] = get[i][0]/1000 #原資料為毫秒，需除以1000換為秒
            if 1666569600>get[i][0]>1106006400: # 2005-01-19 ~ 2022-10-23
                t = time.localtime(get[i][0]) 
                ts = time.strftime("%Y-%m-%d", t) #轉為字串
                data.append([ts,get[i][4]])
        data = pd.DataFrame(data,columns=['DateD',code])
        return data 

    # Unit 1-2 : Crawler Part : Web

    elif code == "CCI":
        url = url[0]    
    elif code == "CPI":
        url = url[1]
    elif code == "FR":
        url = url[2]
    elif code == "UR":
        url = url[3]
    resp = req.Request(url,headers=header)
    with req.urlopen(resp) as res:
        result = res.read().decode("utf-8")
    result = json.loads(result)
    data = result["data"]
    data = stemp2str(data)
    data = pd.DataFrame(data,columns=['DateM',code])
    return data

if __name__ == '__main__':
    code = input("SP500/CPI/CCI/UR/VIX/FR/USD")
    data = uscrawler(code)
    print(data)
    print(type(data))