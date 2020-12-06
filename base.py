import datetime
import json
import time

import requests


# 判断是否是假期
def isHoliday(day):
    timeArray = time.strptime(day, "%Y-%m-%d")
    otherStyleTime = time.strftime("%Y%m%d", timeArray)
    server_url = "http://www.easybots.cn/api/holiday.php?d="
    req = requests.get(server_url + otherStyleTime)
    vop_data = json.loads(req.content)

    if vop_data[otherStyleTime] == '0':
        return True
    elif vop_data[otherStyleTime] == '1':
        return False
    elif vop_data[otherStyleTime] == '2':
        return False
    else:
        return False


# 计算两个时间相减
def myDate(date1, date2):
    date1 = time.strptime(date1, "%H:%M:%S")
    date2 = time.strptime(date2, "%H:%M:%S")

    startTime = time.strftime("%H:%M:%S", date1)
    endTime = time.strftime("%H:%M:%S", date2)

    startTime = datetime.datetime.strptime(startTime, "%H:%M:%S")
    endTime = datetime.datetime.strptime(endTime, "%H:%M:%S")
    date = endTime - startTime
    return date


class Core:
    BASE_URL = "https://kq-oa.percent.cn/api/insurance/query_real_time/"

    def __init__(self, cookie):
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "kq-oa.percent.cn",
            "Origin": "https://kq-oa.percent.cn",
            "Referer": "https://kq-oa.percent.cn/app/attendance/mine",

            "Content-Type": "application/json; charset=utf-8",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.66 Safari/537.36 "
        }

    def get_date(self, date):
        data = {
            "employeeid": "",
            "work_day": str(date),
            "next": "/api/insurance/query_real_time/"
        }
        data = json.dumps(data)
        html = requests.post(url=self.BASE_URL, headers=self.headers, data=data, verify=False)
        res = html.json()
        # 解析的数据
        htmlData = res['data']
        if htmlData is not None:
            d1 = htmlData[0]['time']
            d2 = htmlData[1]['time']
            print(myDate(d1, d2).seconds)
            return myDate(d1, d2).seconds
        else:
            return None

    def run(self):
        # 年月日
        year = time.strftime("%Y")
        month = time.strftime("%m")
        nowDay = time.strftime("%d")

        # 这个月开始结束时间
        begin = datetime.date(int(year), int(month), 1)
        end = datetime.date(int(year), int(month), int(nowDay))

        # 共多少秒
        seconds = 0
        # 这个月工作共多少天
        days = 0
        for i in range((end - begin).days):
            day = begin + datetime.timedelta(days=i)
            tt = time.strptime(str(day), '%Y-%m-%d')
            # 周天
            if not (tt.tm_wday < 6):
                # 判断是否节假日
                pass
                # if isHolide(str(day)):
                #     index += 1
                #     print(str(day))
                #     sec += self.get_date(str(day))
            else:
                if isHoliday(str(day)):
                    try:
                        seconds += self.get_date(str(day))
                        if seconds is not None:
                            days += 1
                            print(str(day))
                    except Exception as e:
                        print(e)
        return round(seconds / 3600 / days, 4)
