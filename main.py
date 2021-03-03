# 重写deal
# 更新函数que，确保运行时间
#

from tkinter import *
import websocket
import json
import zlib
import time
import datetime
try:
    import thread
except ImportError:
    import _thread as thread
import pandas as pd
from queue import Queue
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib
from matplotlib.pylab import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
# %matplotlib qt4

#proces_data(E, G, from_proce_to_dealfuc_que)
# 函数功能：当E从True变为False时，从全局变量Tem中拿到已经积累的弹幕信息，进行去重以及计数处理并重新赋值Tem,通过to_dealfuc传走
# 运行过程：
# E.wait(),在E值为True时，程序启动.声明用于保存弹幕信息的Tem全局变量后进入死循环内部；
# 进入第一个if判断：E为True,启动时程序进入G.wait()程序暂停;直到False则进入第二if判断：
# 当E为False后，执行第二if判断内语句:判断Tem长度是否为0，如果为0，则在to_dealfuc_que中放入（0，0）,进入***E.wait()***防止程序在E值为False时重复执行
# 当E再次从False变为True后，进入死循环的第一if判断语句中的G.wait(),准备再次进入第二if判断执行put
# 当执行第二if判断内语句:判断Tem长度不为0时，执行去重计数语句得到结果Tem_3
# 将Tem重新设置为空df,将Tem_3中的信息put后进入***E.wait()***防止程序在E值为False时重复执行

# control_fuc(E, G)t0
# 函数功能：定时设置事件锁EG，E的初始值为False,G为True.
# 运行过程：
# 当程序开始后,前十分钟无动作，第十分钟开始后将把E和G设置为True\False，五分钟后再修改为初始值

# ws.run_forever()t1
# 函数功能：从网站获取信息处理后通过on_message传给handler

#handler(i, E, from_handler_to_accdata_que)
# 函数功能：将特定条件的网站信息在E锁为True时，提取用户名、弹幕等内容通过to_accdata_que传给acc_data
# 运行过程：
# 每次出现网站信息，时会运行一次，首先判断当前事件锁E是否打开，如果事件锁E未打开那么，handler本次结束。在下次网站信息出现后再次运行
# 当事件锁E开启，则说明当前属于弹幕接受时段
# 进入第一次if判断，判断网站信息的cmd项是否为danmu,如当前cmd项为danmu，则提取其中用户名、弹幕等项打包为字典danmu，进入danmu内容的第二次if判断
# 当danmu内容符合条件时，将把danmu通过to_accdata_que穿给acc_data，本次函数结束

# acc_data(from_handler_to_accdata_que, E)t3 #因为get有控制属性，存在重复控制，可修改
# 函数功能：当E为True时，不断从que中，获取弹幕信息积累全局Tem
# 运行过程：
# 声明用于保存弹幕信息的Tem全局变量后进入死循环内部
# E为False时，死循环内部在E.wait()停止
# 当E为True时，E.wait()结束，并进入死循环后的第二层循环while E.isSet()
# 从to_accdata_que中获得字典信息将获取的danmu加入既有Tem

# deal_fuc(E, G, DEAL, from_proce_to_dealfuc_que, from_deal_to_tk_que)t4
# 函数功能：在最后一刻清仓并重新交易
# 运行过程:
# E.wait(),在E值为True时，程序启动.进入死循环内部；
# 进入第一个if判断：E为True,启动时程序进入G.wait()程序暂停;直到False则进入第二if判断：
# 当E为False后，执行第二if判断内语句:
# 清仓
# 通过to_dealfuc_que获取计票结果，
# 进入计票结果的交易方向判断语句：通过DEAL对应方法执行交易后，将计票结果通过to_tk_que传走
# 进入E.wait()防止程序在E值为False时重复执行

# Tk_fuc(from_deal_to_tk_que,driver,DEAL)t5
# 函数功能：设置UI布局，通过update_time,update_text,update_price实现时间，标签，价格、账户价值的更新
# 运行过程:
# 创建用于存放交易历史显示的hist_list列表
# 设置widget
# 定义update_time,update_text,update_price函数
# 其中update_text用于更新投票人数、仓位、计票时间段、交易历史显示
# 其中update_price用于价格、账户价值显示，
# 在死循环中，每.2s秒执行一次DEAL的刷新方法，通过driver和DEAL获取价格、账户价值

# 总程序运行过程：
# 网站出现有效信息时通过handler函数的 from_handler_to_accdata_que 将***计票时段内的***有效信息传给acc_data
# acc_data将通过 from_handler_to_accdata_que 获得的内容并入Tem
# proces_data会在控制周期i的结束时刻（True变为False时）取走Tem并加工出投票结果
# *在控制周期i+1的开始时刻*将计票加工结果通过 from_proce_to_dealfuc_que 传给deal_fuc后进入E.wait()直到控制周期i+1的结束时刻再次运行
# 当deal_fuc在控制周期i的结束时刻清仓并进入 from_proce_to_dealfuc_que 获取等待，获取到计票加工结果后
chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(r'C:\Users\l\chromedriver',
#                           chrome_options=chrome_options)
# font = {'size': 22}
# matplotlib.rc('font', **font)

driver = webdriver.Chrome(r'C:\Users\l\chromedriver')

driver.get(r'https://www.huobi.be/zh-cn/exchange/btc_usdt/')

websocket_url = 'wss://tx-bj-live-comet-01.chat.bilibili.com/sub'

send1 = [
    0x00, 0x00, 0x01, 0x0F, 0x00, 0x10, 0x00, 0x01, 0x00, 0x00, 0x00, 0x07,
    0x00, 0x00, 0x00, 0x01, 0x7B, 0x22, 0x75, 0x69, 0x64, 0x22, 0x3A, 0x39,
    0x38, 0x38, 0x36, 0x32, 0x39, 0x39, 0x33, 0x2C, 0x22, 0x72, 0x6F, 0x6F,
    0x6D, 0x69, 0x64, 0x22, 0x3A, 0x31, 0x32, 0x39, 0x35, 0x35, 0x37, 0x38,
    0x35, 0x2C, 0x22, 0x70, 0x72, 0x6F, 0x74, 0x6F, 0x76, 0x65, 0x72, 0x22,
    0x3A, 0x32, 0x2C, 0x22, 0x70, 0x6C, 0x61, 0x74, 0x66, 0x6F, 0x72, 0x6D,
    0x22, 0x3A, 0x22, 0x77, 0x65, 0x62, 0x22, 0x2C, 0x22, 0x63, 0x6C, 0x69,
    0x65, 0x6E, 0x74, 0x76, 0x65, 0x72, 0x22, 0x3A, 0x22, 0x32, 0x2E, 0x36,
    0x2E, 0x32, 0x35, 0x22, 0x2C, 0x22, 0x74, 0x79, 0x70, 0x65, 0x22, 0x3A,
    0x32, 0x2C, 0x22, 0x6B, 0x65, 0x79, 0x22, 0x3A, 0x22, 0x34, 0x52, 0x67,
    0x55, 0x70, 0x33, 0x4E, 0x59, 0x6E, 0x7A, 0x6C, 0x50, 0x6F, 0x58, 0x57,
    0x78, 0x5A, 0x45, 0x6D, 0x49, 0x77, 0x4E, 0x4D, 0x32, 0x36, 0x79, 0x77,
    0x7A, 0x5F, 0x76, 0x71, 0x51, 0x6B, 0x46, 0x54, 0x76, 0x6E, 0x50, 0x77,
    0x48, 0x68, 0x4C, 0x6F, 0x62, 0x35, 0x58, 0x77, 0x4C, 0x67, 0x32, 0x56,
    0x59, 0x63, 0x53, 0x44, 0x47, 0x6D, 0x4F, 0x69, 0x67, 0x7A, 0x64, 0x79,
    0x45, 0x48, 0x69, 0x7A, 0x35, 0x59, 0x79, 0x79, 0x30, 0x77, 0x4E, 0x6A,
    0x52, 0x45, 0x51, 0x35, 0x2D, 0x6B, 0x36, 0x62, 0x42, 0x4A, 0x5A, 0x4E,
    0x61, 0x72, 0x75, 0x76, 0x54, 0x75, 0x4F, 0x30, 0x59, 0x42, 0x34, 0x32,
    0x79, 0x6F, 0x46, 0x75, 0x4D, 0x4A, 0x67, 0x4C, 0x75, 0x30, 0x31, 0x30,
    0x4C, 0x32, 0x2D, 0x76, 0x39, 0x47, 0x4C, 0x74, 0x59, 0x52, 0x5A, 0x31,
    0x42, 0x47, 0x70, 0x50, 0x57, 0x36, 0x30, 0x4E, 0x73, 0x76, 0x30, 0x30,
    0x78, 0x69, 0x41, 0x4E, 0x39, 0x63, 0x77, 0x4A, 0x75, 0x79, 0x58, 0x44,
    0x34, 0x7A, 0x6A, 0x38, 0x51, 0x22, 0x7D
]
# ye11owtail
send2 = [
    0x00, 0x00, 0x00, 0x1F, 0x00, 0x10, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x01, 0x5B, 0x6F, 0x62, 0x6A, 0x65, 0x63, 0x74, 0x20,
    0x4F, 0x62, 0x6A, 0x65, 0x63, 0x74, 0x5D
]


def getprice():
    #print('getprice被调用'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return float(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/main/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/dl/dd/div[1]/dl/dt"
        ).text)


l = threading.Lock()


class deal():
    cash = 100000
    position = 0
    margin = 0

    leverage = 1

    totalvalue = 100000
    lastprice = 0  # 如果出现故障则以旧价格交易
    dealhistory = ['', '', '', '']  # 因为后面有insert，所以列表长度为4，插入后长度为5

    def __init__(self, name):
        l.acquire()
        self.name = name
        print('deal类已创建' +
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        l.release()

    def buyfuc(self, lvg=1):

        try:
            l.acquire()
            deal.leverage = lvg
            try:
                price = getprice()
                deal.lastprice = price
            except:
                print('buyfuc中getprice error')
                price = deal.lastprice
            deal.margin = deal.cash
            deal.position = deal.leverage * deal.margin / price  # 全仓多

            deal.cash = 0  # 现金清零
            deal.totalvalue = deal.margin + \
                (deal.position*price - deal.margin*deal.leverage)+ deal.cash
            deal.dealhistory.insert(
                0, (datetime.datetime.now().strftime('%H:%M:%S') +' '+
                    str(deal.leverage) + 'x杠杆' + r' 做多 @ $' + str(price) +
                    ' 数量：' + str(deal.position)[:7]))  # 记录交易
            deal.dealhistory = deal.dealhistory[0:5]

            # print('清空后deal类的仓位、现金、保证金、价值为', deal.position, deal.cash,
            #          deal.margin, deal.totalvalue)
            l.release()
        except:
            print('buyfuc error')

    def shortfuc(self, lvg=1):
        try:
            l.acquire()
            deal.leverage = lvg
            try:
                price = getprice()  # 如果股票代码不存在，tushare服务器返回none
                deal.lastprice = price
            except:
                print('shortfuc中getprice error')
                price = deal.lastprice
            deal.margin = deal.cash
            deal.position = -(deal.leverage * deal.margin / price)  # 全仓空
            deal.cash = 0  # 现金清零
            deal.totalvalue = deal.margin + \
                    (deal.margin*deal.leverage + deal.position*price)+deal.cash
            deal.dealhistory.insert(
                0, (datetime.datetime.now().strftime('%H:%M:%S')+' '+
                    str(deal.leverage) + r'x杠杆' + r' 做空 @ $' + str(price) +
                    ' 数量：' + str(deal.position)[:7]))  # 记录交易
            deal.dealhistory = deal.dealhistory[0:5]
            # print('清空后deal类的仓位、现金、保证金、价值为', deal.position, deal.cash,
            #          deal.margin, deal.totalvalue)
            l.release()
        except:
            print('shortfuc error')

    def liquidation(self):
        try:
            # print('清空前deal类的仓位、现金、保证金、价值为',deal.position,deal.cash,deal.margin,deal.totalvalue)
            l.acquire()
            try:
                price = getprice()  # 如果股票代码不存在，tushare服务器返回none
                deal.lastprice = price
            except:
                print('liquidation中getprice error')
                price = deal.lastprice
            if deal.position < 0:
                deal.cash = deal.margin + \
                    (deal.margin*deal.leverage + deal.position*price)+deal.cash
                deal.position = 0
                deal.margin = 0
                deal.totalvalue = deal.cash
                deal.leverage = 1
                deal.dealhistory.insert(
                    0, (datetime.datetime.now().strftime('%H:%M:%S') +' '+
                        str(deal.leverage) + r'x杠杆' + r' 清仓 @ $' + str(price) +
                        ' 获得现金：$' + str(deal.cash)[:11]))  # 记录交易)
                deal.dealhistory = deal.dealhistory[0:5]

            else:
                deal.cash = deal.margin + \
                    (deal.position*price - deal.margin*deal.leverage)+deal.cash
                deal.position = 0
                deal.margin = 0
                deal.totalvalue = deal.cash
                deal.dealhistory.insert(
                    0, (datetime.datetime.now().strftime('%H:%M:%S') +' '+
                        str(deal.leverage) + r'x杠杆' + r' 清仓 @ $' + str(price) +
                        ' 获得现金：$' + str(deal.cash)[:11]))  # 记录交易
                deal.dealhistory = deal.dealhistory[0:5]


            l.release()
        except:
            print('liquidation error')

    def refresh(self):
        # print('执行deal的刷新操作'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        l.acquire()
        price = getprice()
        deal.lastprice = price
        if deal.position < 0:
            deal.totalvalue = deal.margin + \
                (deal.margin*deal.leverage + deal.position*price)
        else:
            deal.totalvalue = deal.margin + \
                (deal.position*price - deal.margin*deal.leverage)
        result = deal.totalvalue
        l.release()
        return result


# 主函数区间
Tem = pd.DataFrame()  # 创建全局Tem
E = threading.Event()  # 创建事件锁E
E.clear()  # 设置E初始值为False
G = threading.Event()  # 创建事件锁G
G.set()  # 设置G初始值为True
F = threading.Event()  # 创建事件锁F
F.clear()  # 设置F初始值为False,用来同意子函数开始时间
from_handler_to_accdata_que = Queue()  # 创建用来传输单个danmu的queue
from_proce_to_dealfuc_que = Queue()  # 创建用传输整体的Tem的que
from_deal_to_tk_que = Queue()  # 创建传输交易结果的que

DEAL = deal('BTC')
########################################################################


def deal_fuc(E, G, DEAL, from_proce_to_dealfuc_que, from_deal_to_tk_que):
    # deal_fuc责任 在最后一刻清仓并重新交易
    # 程序开始时，isSet为False,程序进入判断二修改flag为True后跳出，当isSet不变时会一直跳过判断一和判断二
    # 当isSet从False变为True时，程序先进入判断一，确保flag为False,依旧不会进入判断二，但开始为下次isSet改变值准备条件
    # 当isSet从True变为False,程序跳过判断一，进入判断二
    print('进入deal_fuc' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    E.wait()
    while True:
        if E.isSet() == True:  # 判断一
            G.wait()
        if E.isSet() == False:  # 判断二
            DEAL.liquidation()
            print('在deal_fuc中，执行deal类清空操作' +
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result = from_proce_to_dealfuc_que.get()
            print(
                '在deal_fuc中，从to_dealfuc_que获得result' +
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), result)
            if result[0] >= result[1]:
                DEAL.buyfuc(15)
                print('在deal_fuc中，执行deal类买操作' +
                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                time.sleep(1)  # 暂停原因：留出一定时间在操作结束后Tk_fuc读取DEAL.position

                from_deal_to_tk_que.put(result)
                E.wait()
            else:
                DEAL.shortfuc(15)
                print('在deal_fuc中，执行deal类卖操作' +
                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                time.sleep(1)  # 暂停原因：留出一定时间在操作结束后Tk_fuc读取DEAL.position

                from_deal_to_tk_que.put(result)

                E.wait()


def decode_json(msg):
    return json.loads(msg[16:])


def decomp(msg):
    try:
        return zlib.decompress(msg[16:])
    except Exception:
        print('error in decomp : {}'.format(msg[16:]))


def decode_msg(msg):
    if len(msg) == 16:
        return []
    if len(msg) == 20:
        return []
    try:
        return [decode_json(msg)]
    except Exception:
        temp = decomp(msg)
        return [json.loads(i) for i in split_jsons(temp)]


def split_jsons(test_msg_4):
    activate = 1
    stack = 0
    start = []
    end = []
    escape = 0
    i = 16
    while i < len(test_msg_4):
        if test_msg_4[i] == 34 and escape % 2 != 1:
            activate = 1 - activate
            i += 1
            continue
        if test_msg_4[i] == 92:
            escape += 1
        else:
            escape = 0
        if activate:
            if test_msg_4[i] == 123:
                if stack == 0:
                    start.append(i)
                stack += 1
            if test_msg_4[i] == 125:
                stack -= 1
                if stack == 0:
                    end.append(i)
                    i += 16
        i += 1
    result = []
    for i2 in range(len(start)):
        try:
            result.append(test_msg_4[start[i2]:end[i2] + 1])
        except Exception:
            print('error while append bytes to result at split_jsons.')
            print('start & end : {},{}'.format(start, end))
            print('msg : \n{}'.format(test_msg_4))
    return result


def on_message(ws, message):
    try:
        [
            handler(i, E, from_handler_to_accdata_que)
            for i in decode_msg(message)
        ]
    except:
        pass


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        ws.send(bytes(send1))
        while True:
            ws.send(bytes(send2))
            time.sleep(30)

    thread.start_new_thread(run, ())


def handler(msg, E, from_handler_to_accdata_que
            ):  # 拿到包含弹幕的内容，当事件锁开启时，只要执行内容验证操作符合就通过queue传走
    print('进入handler中' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if E.isSet():
        #         print('在handler中进入弹幕判断程序' +
        #               datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)
        if msg['cmd'] == 'DANMU_MSG':
            danmu = {
                'msg': msg['info'][1],
                'uid': msg['info'][2][0],
                'id': msg['info'][2][1]
            }
            print(
                '在handler中出现弹幕' +
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), danmu)

        if (danmu['msg'] == '$') or (danmu['msg'] == '#'):
            from_handler_to_accdata_que.put(danmu)
            print(
                '在handler中终于出现符合条件弹幕！！！！！！！！！！！！！！！！！！！！！！！！！' +
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), danmu)
    else:
        pass


def proces_data(E, G, from_proce_to_dealfuc_que):
    global Tem
    E.wait()
    print('进入proces_data' +
          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        try:
            if E.isSet == True:
                G.wait()
                print('In proces_data G.wait() ended' +
                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if E.isSet() == False:
                print('Entered proces_data second judgement' +
                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                if len(Tem) == 0:
                    from_proce_to_dealfuc_que.put(
                        (0, 0))  # 放入一个元组，第一位为看多人数，第二位为看空人数
                    print(
                        '在proces_data中to_dealfuc_que放入内容' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        (0, 0))
                    E.wait()
                else:
                    # 去重得到无重复内容的series
                    Tem_drop_dup = Tem['uid'].drop_duplicates()
                    print(
                        'Tem_drop_dup已结束' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        Tem_drop_dup)
                    # 以series的index得到新的无重复uid内容的dataframe
                    Tem_2 = Tem.iloc[Tem_drop_dup.index]
                    print(
                        'Tem_2已新建' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        Tem_2)
                    # 将新的dataframe按msg中的数量多少得到series（投票内容msg为index和重复次数为value）
                    Tem_3 = Tem_2['msg'].value_counts()
                    Tem = pd.DataFrame()
                    #                     print('Tem_3已新建' +
                    #                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Tem_3)
                    try:
                        print('在proces_data中进入第二个try,做多人数为', Tem_3['$'])
                        LONG = Tem_3['$']
                    except:
                        LONG = 0
                    try:
                        print('在proces_data中进入第三个try,做空人数为', Tem_3['#'])
                        SHORT = Tem_3['#']
                    except:
                        SHORT = 0

                    from_proce_to_dealfuc_que.put(
                        (LONG, SHORT))  # 放入一个元组，第一位为看多人数，第二位为看空人数
                    print(
                        '在proces_data中to_dealfuc_que放入内容' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        (LONG, SHORT))
                    E.wait()
        except:
            pass
            print('进入except,当前Tem长度为 ' + str(len(Tem)),
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def acc_data(from_handler_to_accdata_que, E):  # !!!!!!!!!!!!!!!
    global Tem
    print('进入acc_data中' +
          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        E.wait()
        while E.isSet():
            print('在acc_data中进入isSet判断' +
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            danmu = from_handler_to_accdata_que.get()  # 假如只有一条弹幕，那么程序会卡死在get
            print('在acc_data中通过handledata_que获得信息', danmu)
            Tem = Tem.append(danmu, ignore_index=True)
            print('在acc_data中循环生成的DF', Tem)


def control_fuc(E, G):

        def task_(s, E,G):
            def task__():
                #print('E is '+str(E.isSet()) +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                time.sleep(600)
                E.set()
                G.clear()
                #print('E is '+str(E.isSet()) +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                time.sleep(s)
                E.clear()
                G.set()  # G事件锁打开,E打开
                #print('E is '+str(E.isSet()) +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return task__
        
        sche_00 = BackgroundScheduler()
        sche_00.add_job(task_(299, E,G), 'cron', hour='*',
                        minute='0', second='0', id='task1')
        sche_00.start()
        
        sche_15 = BackgroundScheduler()
        sche_15.add_job(task_(299, E,G), 'cron', hour='*',
                        minute='15', second='0', id='task2')
        sche_15.start()
        
        sche_30 = BackgroundScheduler()
        sche_30.add_job(task_(299, E,G), 'cron', hour='*',
                        minute='30', second='0', id='task3')
        sche_30.start()
        
        sche_45 = BackgroundScheduler()
        sche_45.add_job(task_(299, E,G), 'cron', hour='*',
                        minute='45', second='0', id='task4')
        sche_45.start()
        
        
        

#     def task_(s, E, G):
#         def task__():
#             time.sleep(15)
#             E.set()  # 事件锁打开
#             G.clear()
#             #print('事件锁打开E is OPEN'+str(E.isSet()) +datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))
#             time.sleep(s)
#             E.clear()  # 事件锁关闭
#             G.set()
#             #print('事件锁关闭E is SHUT'+str(E.isSet()) +datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

#         return task__

#     sche_00 = BackgroundScheduler()
#     sche_00.add_job(task_(15, E, G),
#                     'cron',
#                     hour='*',
#                     minute='*',
#                     second='0',
#                     id='task1')
#     sche_00.start()

#     sche_30 = BackgroundScheduler()
#     sche_30.add_job(task_(15, E, G),
#                     'cron',
#                     hour='*',
#                     minute='*',
#                     second='30',
#                     id='task1')
#     sche_30.start()


def Tk_fuc(from_deal_to_tk_que, driver, DEAL):  #
    print('进入Tk_fuc' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    hist_list = ['', '', '', '', '']

    root = Tk()
    root.title("to da moon")
    root.geometry('600x800')
    a = 600
    #root.iconbitmap(r'D:\r5.ico')

    # 标签放置顺序持仓标签、计票时段标签、价格标签、人数说明标签、人数标签、时间标签、sb标签
    time_label = Label(root, text='time_label', bg='red',
                       fg='white')  # 时间标签，背景颜色随持仓改变

    center_label = Label(root,
                         text='当前持仓:\n 0',
                         font="Helvetica 30",
                         fg='yellow',
                         bg='grey')  # 持仓标签，背景不变
    notify_label = Label(root,
                         text='计票时间段\n00:00--00:00',
                         font="Helvetica 15",
                         bg='grey',
                         fg='yellow')  # 计票时间段标签，背景不变
    price_label = Label(root,
                        text='$50000',
                        font="Helvetica 30",
                        bg='black',
                        fg='yellow')  # 价格标签，背景不变

    price_label.place(x=400 / 800 * a,
                      y=300 / 800 * a,
                      height=80 / 800 * a,
                      width=260 / 800 * a,
                      anchor='center')  # 价格标签放置
    center_label.place(x=400 / 800 * a,
                       y=410 / 800 * a,
                       height=240 / 800 * a,
                       width=260 / 800 * a,
                       anchor='center')  # 持仓标签放置
    notify_label.place(x=400 / 800 * a,
                       y=507 / 800 * a,
                       height=90 / 800 * a,
                       width=260 / 800 * a,
                       anchor='center')  # 计票时间段标签放置

    # 持仓围栏
    c_label_1 = Label(root, bg='white')
    c_label_2 = Label(root, bg='white')
    c_label_3 = Label(root, bg='white')
    c_label_4 = Label(root, bg='white')
    c_label_1.place(x=400 / 800 * a,
                    y=307.5,
                    height=4,
                    width=260 / 800 * a,
                    anchor='center')  # -
    c_label_2.place(x=400 / 800 * a,
                    y=350,
                    height=4,
                    width=260 / 800 * a,
                    anchor='center')  # -
    c_label_3.place(x=208.25,
                    y=410 / 800 * a + 21.5,
                    height=42.5,
                    width=4,
                    anchor='center')  # |
    c_label_4.place(x=600 - 208.25,
                    y=410 / 800 * a + 21.5,
                    height=42.5,
                    width=4,
                    anchor='center')  # |

    label_r_l = Label(root,
                      text="看空人数",
                      font="Helvetica 30",
                      bg='blue',
                      fg='grey')  # 人数说明标签，背景不变
    label_l_l = Label(root,
                      text="看多人数",
                      font="Helvetica 30",
                      bg='blue',
                      fg='grey')  # 人数说明标签，背景不变

    label_r_n = Label(root,
                      text="100",
                      font="Helvetica 30",
                      bg='red',
                      fg='yellow')  # 人数说明标签，背景不变
    label_l_n = Label(root,
                      text="100",
                      font="Helvetica 30",
                      bg='green',
                      fg='yellow')  # 人数说明标签，背景不变

    label_l_n.place(x=135 / 800 * a,
                    y=440 / 800 * a,
                    height=260 / 800 * a,
                    width=280 / 800 * a,
                    anchor='center')  # 人数标签放置
    label_r_n.place(x=665 / 800 * a,
                    y=440 / 800 * a,
                    height=260 / 800 * a,
                    width=280 / 800 * a,
                    anchor='center')  # 人数标签放置
    label_l_l.place(x=135 / 800 * a,
                    y=285 / 800 * a,
                    height=50 / 800 * a,
                    width=280 / 800 * a,
                    anchor='center')  # 人数说明标签放置
    label_r_l.place(x=665 / 800 * a,
                    y=285 / 800 * a,
                    height=50 / 800 * a,
                    width=280 / 800 * a,
                    anchor='center')  # 人数说明标签放置

    time_label.place(x=400 / 800 * a,
                     y=130 / 800 * a,
                     height=260 / 800 * a,
                     width=800 / 800 * a,
                     anchor='center')  # 放置时间标签

    s_1 = Label(root,
                text="This is a status bar",
                font="Helvetica 15",
                relief='sunken',
                fg='white',
                bg='grey')
    s_2 = Label(root,
                text="This is a status bar",
                font="Helvetica 15",
                relief='sunken',
                fg='white',
                bg='black')
    s_3 = Label(root,
                text="This is a status bar",
                font="Helvetica 15",
                relief='sunken',
                fg='white',
                bg='grey')
    s_4 = Label(root,
                text="This is a status bar",
                font="Helvetica 15",
                relief='sunken',
                fg='white',
                bg='black')
    s_5 = Label(root,
                text="This is a status bar",
                font="Helvetica 15",
                relief='sunken',
                fg='white',
                bg='grey')

    sb_list = [s_1, s_2, s_3, s_4, s_5]

    def update_time():
        """更新时间"""
        current_time = time.strftime("%H:%M:%S")
        time_label.config(text=current_time, font="Helvetica 90")
        time_label.after(200, update_time)

    def update_text():
        try:
            print(('在tk_fuc中启动updatetext') +
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            while True:
                result = from_deal_to_tk_que.get()
                print('在TK_fuc进入while循环中，从from_deal_to_tk_que获得信息', result,
                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                label_r_n.config(text=str(result[1]))
                label_l_n.config(text=str(result[0]))

                print('在tkfuc中获取到DEAL.position', DEAL.position)
                center_label.config(text='当前持仓:\n' +
                                    str(round(float(DEAL.position), 2)))
                if result[0] >= result[1]:
                    time_label.config(bg='green')
                else:
                    time_label.config(bg='red')

                print('在tkfuc修改notify_label', DEAL.dealhistory)
                notify_label.config(
                    text='本轮计票时间段:\n' + time.strftime(
                        '%H:%M', time.localtime(int(time.time()) + 600)) +
                    '-' + time.strftime(
                        '%H:%M', time.localtime(int(time.time()) + 900)))
                content_for_sb = DEAL.dealhistory
                print('在tkfuc中获取到DEAL.dealhistory', DEAL.dealhistory)
                for i in range(5):
                    sb_list[i].config(text=content_for_sb[i])
        except:
            print('update_text error')

    def update_price():
        while True:
            try:
                # print('进入Tk_fuc中的update_price'+datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))
                time.sleep(0.5)
                DEAL.refresh()
                price_label.config(text='$' + str(
                    float(
                        driver.find_element_by_xpath(
                            "/html/body/div[1]/div/div/main/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/dl/dd/div[1]/dl/dt"
                        ).text)))
                value = DEAL.totalvalue
                value_label_n.config(text='当前价值：$' + str(value))
                if value >= 100000:
                    value_label_n.config(bg='green')
                else:
                    value_label_n.config(bg='red')
            except:
                pass

    threading.Thread(target=update_time).start()
    threading.Thread(target=update_text).start()
    threading.Thread(target=update_price).start()

    value_label_l = Label(root,
                          text='初始价值：$100000',
                          font="Helvetica 30",
                          bg='pink',
                          fg='grey')
    value_label_n = Label(root,
                          text='当前价值：$100000',
                          font="Helvetica 30",
                          bg='green',
                          fg='yellow')

    value_label_l.place(x=400 / 800 * a,
                        y=507 / 800 * a + 80,
                        height=135 / 800 * a,
                        width=800 / 800 * a,
                        anchor='center')
    value_label_n.place(x=400 / 800 * a,
                        y=507 / 800 * a + 175,
                        height=130 / 800 * a,
                        width=800 / 800 * a,
                        anchor='center')

    s_1.place(x=400 / 800 * a,
              y=560 / 800 * a + 206,
              height=45 / 800 * a,
              width=800 / 800 * a,
              anchor='center')
    s_2.place(x=400 / 800 * a,
              y=605 / 800 * a + 206,
              height=45 / 800 * a,
              width=800 / 800 * a,
              anchor='center')
    s_3.place(x=400 / 800 * a,
              y=650 / 800 * a + 206,
              height=45 / 800 * a,
              width=800 / 800 * a,
              anchor='center')
    s_4.place(x=400 / 800 * a,
              y=695 / 800 * a + 206,
              height=45 / 800 * a,
              width=800 / 800 * a,
              anchor='center')
    s_5.place(x=400 / 800 * a,
              y=740 / 800 * a + 206,
              height=45 / 800 * a,
              width=800 / 800 * a,
              anchor='center')
    root.mainloop()


####################################################################################################

websocket.enableTrace(True)

ws = websocket.WebSocketApp(websocket_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open

t0 = threading.Thread(target=control_fuc, args=(
    E,
    G,
))
t0.setDaemon(True)

t1 = threading.Thread(target=ws.run_forever)
t1.setDaemon(True)
t2 = threading.Thread(target=proces_data,
                      args=(
                          E,
                          G,
                          from_proce_to_dealfuc_que,
                      ))
t2.setDaemon(True)
t3 = threading.Thread(target=acc_data, args=(
    from_handler_to_accdata_que,
    E,
))
t3.setDaemon(True)
t4 = threading.Thread(target=deal_fuc,
                      args=(
                          E,
                          G,
                          DEAL,
                          from_proce_to_dealfuc_que,
                          from_deal_to_tk_que,
                      ))
t4.setDaemon(True)
t5 = threading.Thread(target=Tk_fuc,
                      args=(
                          from_deal_to_tk_que,
                          driver,
                          DEAL,
                      ))
t5.setDaemon(True)

####################################################################################################
# xiugai


def program_start():
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()


program_start()

# fig = figure(num=0, figsize=(16, 16), dpi=100)
# ax01 = fig.subplots()
# ax01.set_title('')
# ax01.set_ylim(50000000, 100000000)
# ax01.set_xlim(0, 500)
# ax01.grid(True)
# ax01.set_xlabel(" ")
# ax01.set_ylabel("$$$")

# ylist = zeros(0)
# xlist = zeros(0)

# p011, = ax01.plot(xlist, ylist, 'b-', label="$$$")
# ax01.legend([p011], [p011.get_label()])
# x = 0

# def updateData(self):
#     global ylist
#     global x
#     global xlist
#     global DEAL
#     ylist = append(ylist, DEAL.totalvalue)
#     xlist = append(xlist, x)
#     x += 1
#     p011.set_data(xlist, ylist)
#     if x >= 60-40:
#         p011.axes.set_xlim(x-60+40.0, x+40)
#         p011.axes.set_ylim(min(ylist)-5, max(ylist)+5)
#         xlist = xlist[-501:]
#         ylist = ylist[-501:]
#     return p011

# simulation = animation.FuncAnimation(fig, updateData, blit=False, interval=10)
# plt.show()
