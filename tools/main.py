# -*- coding: utf-8 -*-
import json
import os
import re
import threading
import traceback
import wx
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

import sys
import locale
locale.setlocale(locale.LC_ALL, '')

MAIN_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
print(MAIN_FILE_PATH)
BASE_PATH = os.path.dirname(MAIN_FILE_PATH)
print(BASE_PATH)
os.chdir(MAIN_FILE_PATH)
#sys.path.append("../Spiders/")
sys.path.append(os.path.join(BASE_PATH, "./Spiders/"))
DATA_DIR = os.path.join(BASE_PATH, "./data")
try:
    print(DATA_DIR)
    os.mkdir(DATA_DIR)
except OSError:
    pass

# import Scripts.shgjj
# from Spiders.shgjj.main import GjjSpider
from Spiders.A12306 import main12306
from Spiders.JdSpider.jd_more_info import JSpider
from Spiders.alipay.main import ASpider
from Spiders.ctrip.main import Ctrip
from Spiders.mail.main import YSpider
from Spiders.shgjj.main import GjjSpider
from Spiders.taobao.spider import TaobaoSpider
from Spiders.telephone.main import LianTong, DianXin
from Spiders.yidong.main import YiDong


class Button:
    frame = None
    def __init__(self, frame, pnl, item):
        pic_jd = wx.Image(item.img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        btn_jd = wx.BitmapButton(pnl, -1, pic_jd, pos=(item.x, item.y), size=(100, 100))
        # wx.StaticText(pnl, -1, item.title, pos=(item.x + 30, item.y + 110))
        wx.StaticText(pnl, -1, item.title, pos=(item.x, item.y+110), size=(100, 15), style=wx.ALIGN_CENTRE)
        self.frame = frame
        self.frame.Bind(wx.EVT_BUTTON, self.OnClick, btn_jd)

    def Automation(self, url):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=option)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'
        })
        url = str(url)
        self.driver.get(url)
        time.sleep(10)

    def getCookie3(self, login_url, quit):
        self.updateStatus(self.frame,0)
        self.Automation(login_url)
        cookie_str = ''
        while 1:
            time.sleep(0.2)
            if self.driver.current_url != login_url:
                get_cookies = self.driver.get_cookies()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                if quit == 1:
                    self.driver.quit()
                break
        return cookie_str

    def getCookie2(self, login_url, curr_url, extra_url, quit):
        self.updateStatus(self.frame,0)
        self.Automation(login_url)
        cookie_str = ''
        while 1:
            time.sleep(0.2)
            if self.driver.current_url == curr_url:
                # if extra_url == '':
                #     self.driver.get(extra_url)
                get_cookies = self.driver.get_cookies()
                print(get_cookies)
                print()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                if quit == 1:
                    self.driver.quit()
                break
        return cookie_str

    # ???????????? Cookie
    # https://www.zhihu.com/signin
    # https://www.zhihu.com
    # https://www.zhihu.com/hot
    def getCookie4(self, login_url, curr_url, quit):
        self.updateStatus(self.frame, 0)
        self.Automation(login_url)
        cookie_str = ''
        while 1:
            # self.driver.delete_all_cookies()
            time.sleep(10)
            # self.driver.implicitly_wait(5)
            print(self.driver.current_url)
            # if self.driver.current_url == curr_url:
                # get_cookies = self.driver.get_cookies()
            get_cookies = self.driver.get_cookies()
            cookie_str = ''
            for s in get_cookies:
                cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
            # cookie_str = str(get_cookies)
            if (quit == 1) and (cookie_str != ''):
                self.driver.quit()
                break
        return cookie_str


    def getCookie(self, login):
        cookie_list = self.driver.get_cookies()
        res = ''
        for cookie in cookie_list:
            res += cookie.get('name') + '=' + cookie.get('value').replace('\"', '') + ';'
        return res

    def updateStatus(self, frame, status):
        if status == 0:
            frame.SetStatusText("?????????...", 1)
        elif status == 1:
            try:
                self.driver.quit()
            except:
                pass
            frame.SetStatusText("???????????????", 1)
        else:
            try:
                self.driver.quit()
            except:
                pass
            frame.SetStatusText("???????????????", 1)

class JdButton(Button):
    def OnClick(self, event):
        self.updateStatus(self.frame,0)
        url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        self.Automation(url)
        login_element = "[class='user_logout']"
        cookie = self.getCookie(login_element)
        if cookie:
            try:
                spider = JSpider(cookie, DATA_DIR)
                # spider.getAndStoreBoughtItems()
                
                spider.get_creditData()
                spider.get_browseDataNew()
                spider.get_income()
                spider.get_user_info()
                spider.get_addr()
                
                #spider.get_YHK()
                spider.get_xjk_info()
                spider.get_finance_income()
                # spider.get_GB_num()
                spider.get_JY_bill()
                spider.get_follow_shops()
                spider.get_follow_products()
                # spider.get_cart()
                # spider.get_orders()

                self.updateStatus(self.frame, 1)
            except Exception as e:
                traceback.print_exc()
                self.updateStatus(self.frame, 2)
        else:
            self.updateStatus(self.frame, 2)

class ChisButton(Button):
    def OnClick(self, event):
        login_url = 'https://account.chsi.com.cn/passport/login'
        curr_url = 'https://account.chsi.com.cn/account/account!show.action'
        extra_url = 'https://my.chsi.com.cn/archive/index.action'
        cookie_str = self.getCookie2(login_url, curr_url, extra_url, 1)
        if cookie_str == '':
            self.updateStatus(self.frame,2)
            return

        from Spiders.chsi.main import Chis
        try:
        
            chis = Chis(cookie_str)
            p1, p2, x = chis.get_xueji_info()
            chis.save_ret(p1, '???????????????.jpg')
            chis.save_ret(p2, '????????????.jpg')
            chis.save_ret(x, '???????????????.jpg')
            p3 = chis.get_report()
            chis.save_ret(p3, '????????????.pdf')
            self.updateStatus(self.frame,1)
        except Exception:
            self.updateStatus(self.frame,2)

class YidongButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://login.10086.cn/html/login/login.html'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url.startswith('https://shop.10086.cn/i/?f=home&welcome'):
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    self.driver.quit()
                    break
            try:
                y = YiDong(cookie_str)
                y.get_bill_info()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class GjjButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'http://person.shgjj.com/gjjweb/#/login5/A0'
            self.Automation(url)
            while 1:
                try:
                    time.sleep(0.2)
                    if self.driver.current_url == 'http://person.shgjj.com/gjjweb/#/app':
                        # self.driver.minimize_window()
                        # ??????cookie
                        get_cookies = self.driver.get_cookies()
                        cookie_str = ''
                        for s in get_cookies:
                            cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                        break
                except Exception:
                    pass
            token = self.driver.execute_script("return localStorage.getItem('gjj-authenticationToken')")
            token = token.replace('"', '')
            self.driver.quit()
            try:
                t = GjjSpider(cookie_str, token)
                t.get_priaccountForWeb()
                t.get_accountForWeb()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception as e:
            #print(e)
            self.updateStatus(self.frame,2)

class A12306Button(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://kyfw.12306.cn/otn/resources/login.html'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url == 'https://kyfw.12306.cn/otn/view/index.html':
                    time.sleep(2)
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    self.driver.quit()
                    break
            try:
                a = main12306.Info(cookie_str)
                # ???????????????json??????
                a.get_user_info()
                # ???????????????
                a.get_OrderNoComplete()
                # ??????????????? 
                a.get_Order()
                # ?????????
                a.get_passengers()
                # ??????????????????
                a.get_address()
                # ????????????
                # a.get_insurance()
                # ????????????
                a.get_History_Order()
                # ????????????
                # a.get_level()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class CtripButton(Button):
    def OnClick(self, event):
        login_url = 'https://passport.ctrip.com/user/login'
        cookie_str = self.getCookie3(login_url, 1)
        print(cookie_str);
        if cookie_str == '':
            self.updateStatus(self.frame,2)
            return
        y = Ctrip(cookie_str)
        y.get_order()
        self.updateStatus(self.frame,1)

class LiantongButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://uac.10010.com/portal/mallLogin.jsp?redirectURL=http://iservice.10010.com/e4/query/basic/personal_xx_iframe.html'
            self.Automation(url)
            while 1:
                time.sleep(1)
                if self.driver.current_url == 'http://iservice.10010.com/e4/query/basic/personal_xx_iframe.html':
                    self.driver.minimize_window()
                    time.sleep(5)
                    self.driver.get('http://iservice.10010.com/e3/query/basic/personal_xx_iframe.html')
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    break
            try:
                y = LianTong(cookie_str)
                # y.get_user_info()
                y.get_bill_info()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class DianxingButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://login.189.cn/web/login'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    self.driver.minimize_window()
                    self.driver.get('https://service.sh.189.cn/service/account')
                    time.sleep(0.2)
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    break
            try:
                y = DianXin(cookie_str)
                y.get_user_info()
                y.get_bill_info()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)
class WymailButton(Button):
    def OnClick(self, event):
        # try:
        self.updateStatus(self.frame,0)
        url = 'https://mail.126.com/'
        self.Automation(url)
        while 1:
            time.sleep(0.2)
            if self.driver.current_url != url:
                get_cookies = self.driver.get_cookies()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                self.driver.quit()
                break
            # try:
        y = YSpider()
        y.get_wangyi(cookie_str)
        self.updateStatus(self.frame,1)
        #     except Exception:
        #         self.updateStatus(self.frame,2)
        # except Exception:
        #     self.updateStatus(self.frame,2)
class HotmailButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1556600210&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fmail%2finbox%3fnlp%3d1%26RpsCsrfState%3d99f809e4-d908-a164-e17a-a4739e713c63&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015'
            self.Automation(url)
            while 1:
                time.sleep(1)
                if 'https://outlook.live.com/mail/' in self.driver.current_url:
                    time.sleep(1)
                    cookies_list = self.driver.get_cookies()
                    self.driver.quit()
                    break
            # try:
            y = YSpider()
            t = threading.Thread(target=y.get_hotmail, args=(cookies_list,))
            t.start()
            t.join()
            self.updateStatus(self.frame,1)
            # except Exception:
            #     self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class QqmailButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://mail.qq.com/cgi-bin/loginpage'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    # sid = re.findall('sid=(\w+)&?', self.driver.current_url)[0]
                    from urllib import parse
                    sid = parse.parse_qs(parse.urlparse(self.driver.current_url).query)['sid'][0]
                    break
            try:
                y = YSpider()
                t = threading.Thread(target=y.qq_mail, args=(cookie_str, sid))
                t.start()  # ???????????????????????????????????????
                t.join()
                self.updateStatus(self.frame, 1)
            except Exception:
                self.updateStatus(self.frame, 2)
        except Exception:
            self.updateStatus(self.frame, 2)

class AlimailButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://mail.aliyun.com/alimail/auth/login?reurl=%2Falimail%2F'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    self.driver.minimize_window()
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    break
            try:
                y = YSpider()
                t = threading.Thread(target=y.get_aliyun_mail, args=(cookie_str,))
                t.start()
                t.join()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class XlmailButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://mail.sina.com.cn/?from=mail'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    self.driver.minimize_window()
                    time.sleep(2)
                    self.driver.delete_cookie('NowDate')
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    break
            try:
                y = YSpider()
                t = threading.Thread(target=y.sinamail, args=(cookie_str,))
                t.start()  # ???????????????????????????????????????
                t.join()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)

class TaobaoButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://login.taobao.com/'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    self.driver.minimize_window()
                    cookies_list = self.driver.get_cookies()
                    # ??????cookie
                    file_path = '../Spiders/taobao/taobao_cookies.json'
                    cookie_str = json.dumps(cookies_list)
                    self.driver.quit()
                    with open(file_path, 'w') as f:
                        f.write(cookie_str)
                    break
            try:
                cookie_list = json.loads(open(file_path, 'r').read())
                t = TaobaoSpider(cookie_list)

                t.get_addr()
                t.get_choucang_item()
                t.get_footmark_item()
                # t.crawl_good_buy_data()
                self.updateStatus(self.frame,1)
            except Exception:
                traceback.print_exc()
                self.updateStatus(self.frame,2)
        except Exception:
            traceback.print_exc()
            self.updateStatus(self.frame,2)

class ZfbButton(Button):
    def OnClick(self, event):
        try:
            self.updateStatus(self.frame,0)
            url = 'https://auth.alipay.com/login/index.htm'
            self.Automation(url)
            while 1:
                time.sleep(0.2)
                if self.driver.current_url != url:
                    get_cookies = self.driver.get_cookies()
                    cookie_str = ''
                    for s in get_cookies:
                        cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                    self.driver.quit()
                    # print(cookie_str)
                    break
            try:
                spider = ASpider(cookie_str)
                spider.get_bills()
                spider.get_user_info()
                # spider.get_YEB()
                self.updateStatus(self.frame,1)
            except Exception:
                self.updateStatus(self.frame,2)
        except Exception:
            self.updateStatus(self.frame,2)
        
class GithubButton(Button):
    def OnClick(self, event):
        dlg = wx.TextEntryDialog(None, u"?????????Github?????????:", u"??????Github????????????")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        from github.main import Github
        github = Github(message)
        self.updateStatus(self.frame, 0)
        try:
            github.get_user_info()
            github.get_user_repos()
            github.get_user_following()
            github.get_user_followers()
            github.get_user_activity()
            # github.get_user_repos_detail()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass


class QqButton(Button):
    def OnClick(self, event):
        # ????????????????????????
        messagestr = u'''
1. ??????????????????????????????????????????QQ????????????????????????
2. ?????????Q?????????????????????????????????
3. ????????????????????????????????????????????????
4. ???????????????"????????????????????????????????????????????????(??????????????????),?????????json"????????????
        '''
        dlg = wx.MessageDialog(None, messagestr, u"??????????????????", wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Close()
            # self.Close(True)

        from Spiders.qqfriend.main import Qqfriend
        try:
            self.updateStatus(self.frame, 0)
            qq_friend = Qqfriend()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class QqqunButton(Button):
    def OnClick(self, event):
        # ????????????????????????
        messagestr = u'''
1. ??????????????????????????????????????????QQ???????????????????????????
2. ????????????????????????QQ?????????
3. ???????????????"????????????????????????????????????json"????????????
        '''
        dlg = wx.MessageDialog(None, messagestr, u"??????????????????", wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Close()
            
        from qqqun.main import Qqqun
        try:
            self.updateStatus(self.frame, 0)
            qq_qun = Qqqun()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class ZhihuButton(Button):
    def OnClick(self, event):
        
        dlg = wx.TextEntryDialog(None, u"????????????????????????(????????????):", u"????????????????????????")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        ## ?????????message = 'gao-nan-bao'
        self.updateStatus(self.frame, 0)
        from zhihu.main import Zhihu
        try:
            zhihu = Zhihu(message)
            # ????????????????????????
            zhihu.get_user_profile()
            # ????????????????????????
            zhihu.get_user_followees()
            # ?????????????????????
            zhihu.get_user_followers()
            # ???????????????????????????
            zhihu.get_user_articles()
            # ?????????????????????
            zhihu.get_user_collections()
            # ???????????????????????????
            zhihu.get_user_zvideos()
            # ?????????????????????
            zhihu.get_user_activities()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class CloudmusicButton(Button):
    def OnClick(self, event):
        dlg1 = wx.TextEntryDialog(None, u"?????????????????????????????????????????????(??????):", u"?????????????????????")
        if dlg1.ShowModal() == wx.ID_OK:
            username = dlg1.GetValue()  # ??????????????????????????????
        dlg1.Destroy()
        dlg2 = wx.TextEntryDialog(None, u"?????????????????????????????????:", u"?????????????????????", style=wx.TE_PASSWORD|wx.OK|wx.CANCEL)
        if dlg2.ShowModal() == wx.ID_OK:
            password = dlg2.GetValue()  # ??????????????????????????????
        dlg2.Destroy()
        # print(username, password)
        self.updateStatus(self.frame, 0)
        from Spiders.cloudmusic.main import Cloudmusic
        try:
            music = Cloudmusic(username, password)
            music.get_user_detail()
            music.get_playlist()
            music.get_user_follows()
            music.get_user_followeds()
            music.get_user_event()
            music.get_user_record_week()
            music.get_user_record_all()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass


class BilibiliButton(Button):
    def OnClick(self, event):
        self.updateStatus(self.frame,0)
        url = 'https://passport.bilibili.com/login'
        self.Automation(url)
        while 1:
            time.sleep(0.2)
            if self.driver.current_url != url:
                get_cookies = self.driver.get_cookies()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                self.driver.quit()
                break
        from Spiders.bilibili.main import BilibiliHistory
        bili = BilibiliHistory(cookie_str)
        self.updateStatus(self.frame,1)

class WechatButton(Button):
    def OnClick(self, event):
        # ????????????????????????
        messagestr = u'''
????????????????????????????????????????????????.

================??????================
?????????????????????????????????????????????????????????????????????????????????
        '''
        dlg = wx.MessageDialog(None, messagestr, u"????????????", wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Close()

class WechatmomentButton(Button):
    def OnClick(self, event):
        pass

class MomentsalbumButton(Button):
    def OnClick(self, event):
        # ????????????????????????
        messagestr = u'''
--------------------------???????????????---------------------------------
???????????????????????????????????????????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????<????????????>?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

--------------------------????????????---------------------------------
???????????????????????????????????????????????????????????????????????????????????????????????????????????????
???????????????https://chushu.la/book/*********

???????????????????????????????????????????????????????????????
        '''
        dlg = wx.MessageDialog(None, messagestr, u"????????????", wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Close()

            from Spiders.moments_album.main import Momentsablum
            try:
                self.updateStatus(self.frame, 0)
                ma = Momentsablum()
                ma.make_album()
                self.updateStatus(self.frame, 1)
            except:
                self.updateStatus(self.frame, 2)
                pass
        else:
            dlg.Close()

class BrowserButton(Button):
    def OnClick(self, event):
        from Spiders.browser.main import Browserhistory
        try:
            self.updateStatus(self.frame, 0)
            bh = Browserhistory()
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class CnblogButton(Button):
    def OnClick(self, event):
        dlg = wx.TextEntryDialog(None, u"??????????????????????????????:", u"?????????????????????????????????")
        if dlg.ShowModal() == wx.ID_OK:
            blogname = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        from Spiders.cnblog.main import Cnblog
        try:
            self.updateStatus(self.frame, 0)
            cb = Cnblog(blogname)
            article = cb.get_element_of_article()
            json_file_name = cb.save_as_json(article)
            cb.create_wordcloud(json_file_name, title='????????????????????????', column='title')
            cb.create_postdate_line(json_file_name, title='???????????????', column='postdate')
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class CsdnButton(Button):
    def OnClick(self, event):
        dlg = wx.TextEntryDialog(None, u"?????????CSDN??????????????????:", u"??????CSDN????????????????????????")
        if dlg.ShowModal() == wx.ID_OK:
            blogname = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        from Spiders.csdn.main import Csdn
        try:
            self.updateStatus(self.frame, 0)
            csdn = Csdn(blogname)
            article = csdn.get_element_of_article()
            csdn.save_as_json(article)
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass
            
class OschinaButton(Button):
    def OnClick(self, event):
        dlg = wx.TextEntryDialog(None, u"?????????????????????????????????????????????:", u"??????????????????????????????????????????")
        if dlg.ShowModal() == wx.ID_OK:
            blogurl = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        from Spiders.oschina.main import Oschina
        try:
            self.updateStatus(self.frame, 0)
            oschina = Oschina(blogurl)
            article = oschina.get_element_of_article()
            oschina.save_as_json(article)
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class JianshuButton(Button):
    def OnClick(self, event):
        dlg = wx.TextEntryDialog(None, u"?????????????????????????????????:", u"??????????????????????????????")
        if dlg.ShowModal() == wx.ID_OK:
            blogurl = dlg.GetValue()  # ??????????????????????????????
        dlg.Destroy()
        from Spiders.jianshu.main import Jianshu
        try:
            self.updateStatus(self.frame, 0)
            jianshu = Jianshu(blogurl)
            article = jianshu.get_element_of_article()
            jianshu.save_as_json(article)
            self.updateStatus(self.frame, 1)
        except:
            self.updateStatus(self.frame, 2)
            pass

class Item:
    x = 0
    y = 0
    title = ''
    img = ''
    def __init__(self, x, y, title, img):
        self.x = x
        self.y = y
        self.title = title
        self.img = img

class CreateFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(CreateFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # create status bar
        statusBar = self.CreateStatusBar()
        statusBar.SetFieldsCount(2)
        statusBar.SetStatusWidths([-5, -1])

        # create buttons
        # start_x = 149
        # start_y = 25
        # xstep = 200
        # ystep = 150
        start_x = 25
        start_y = 25
        xstep = 125
        ystep = 150
        ## row 1
        GithubButton(self, self.pnl, Item(start_x, start_y, 'Github', 'resource/icon/github.png'))
        QqmailButton(self, self.pnl, Item(start_x+xstep, start_y, 'QQ??????', 'resource/icon/qmail.png'))
        WymailButton(self, self.pnl, Item(start_x+xstep*2, start_y, '????????????', 'resource/icon/wangyi.png'))
        AlimailButton(self, self.pnl, Item(start_x+xstep*3, start_y, '????????????', 'resource/icon/alimail.png'))
        XlmailButton(self, self.pnl, Item(start_x+xstep*4, start_y, '????????????', 'resource/icon/sina.png'))
        HotmailButton(self, self.pnl, Item(start_x+xstep*5, start_y, 'Hotmail/Outlook', 'resource/icon/hotmail.png'))
        ## row 2
        JdButton(self, self.pnl, Item(start_x, start_y+ystep, '??????', 'resource/icon/jd.png'))
        TaobaoButton(self, self.pnl, Item(start_x+xstep, start_y+ystep, '??????', 'resource/icon/taobao.png'))
        ZfbButton(self, self.pnl, Item(start_x+xstep*2, start_y+ystep, '?????????', 'resource/icon/alipay-logo.png'))
        YidongButton(self, self.pnl, Item(start_x +xstep*3, start_y+ystep, '????????????', 'resource/icon/yidong.png'))
        LiantongButton(self, self.pnl, Item(start_x +xstep*4, start_y+ystep, '????????????', 'resource/icon/liantong.png'))
        DianxingButton(self, self.pnl, Item(start_x +xstep*5, start_y+ystep, '????????????', 'resource/icon/dianxin.png'))
        ## row 3
        ZhihuButton(self, self.pnl, Item(start_x, start_y+ystep*2, '??????', 'resource/icon/zhihu.png'))
        BilibiliButton(self, self.pnl, Item(start_x+xstep, start_y+ystep*2, '????????????', 'resource/icon/bilibili.png'))
        CloudmusicButton(self, self.pnl, Item(start_x+xstep*2, start_y+ystep*2, '???????????????', 'resource/icon/netease_cloudmusic.png'))
        QqButton(self, self.pnl, Item(start_x+xstep*3, start_y+ystep*2, 'QQ??????', 'resource/icon/qq.png'))
        QqqunButton(self, self.pnl, Item(start_x+xstep*4, start_y+ystep*2, 'QQ???', 'resource/icon/qqqun.png'))
        MomentsalbumButton(self, self.pnl, Item(start_x+xstep*5, start_y+ystep*2, '?????????????????????', 'resource/icon/wechat-moments-album.png'))
        ## row 4
        BrowserButton(self, self.pnl, Item(start_x, start_y+ystep*3, 'Chrome????????????', 'resource/icon/chrome-logo.png'))
        A12306Button(self, self.pnl, Item(start_x+xstep, start_y+ystep*3, '12306', 'resource/icon/12306.png'))
        CnblogButton(self, self.pnl, Item(start_x+xstep*2, start_y+ystep*3, '?????????', 'resource/icon/cnblog.png'))
        CsdnButton(self, self.pnl, Item(start_x+xstep*3, start_y+ystep*3, 'CSDN??????', 'resource/icon/csdn.png'))
        OschinaButton(self, self.pnl, Item(start_x+xstep*4, start_y+ystep*3, '??????????????????', 'resource/icon/oschina.png'))
        JianshuButton(self, self.pnl, Item(start_x+xstep*5, start_y+ystep*3, '??????', 'resource/icon/jianshu.png'))
        # CtripButton(self, self.pnl, Item(start_x+xstep*2, start_y+ystep*3, '??????', 'resource/icon/ctrip.png'))
        # ChisButton(self, self.pnl, Item(start_x+xstep*3, start_y+ystep*3, '?????????', 'resource/icon/xuexin.png'))
        # WechatButton(self, self.pnl, Item(start_x+xstep*4, start_y+ystep*3, '????????????', 'resource/icon/wechat.png'))
        # WechatmomentButton(self, self.pnl, Item(start_x+xstep*5, start_y+ystep*3, '???????????????', 'resource/icon/wechat-moments.png'))
        # GjjButton(self, self.pnl, Item(start_x +xstep*4, start_y+ystep*2, '?????????', 'resource/icon/gjj.png'))
        
        
        

if __name__ == '__main__':
    """When this module is run (not imported) then create the app, the
    frame, show it, and start the event loop."""
    app = wx.App()
    frm = CreateFrame(None, title='INFO-SPIDER  ????????????  ????????????????????????', size=(800, 700), pos=(20, 20))
    frm.SetBackgroundColour('#E1E1E1')
    frm.Show()
    app.MainLoop()

