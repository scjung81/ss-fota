#!/usr/bin/env om
# coding: utf-8
def start_send_report_email_custom(model_lists, email_list):
    import pandas as pd

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # # 관심 단말 등록

    # In[2]:
    # model_lists = [['SM-G977N'
    #
    #     # email_list = ["58fc60be.o365skt.onmicrosoft.com@apac.teams.ms", "jungil.kwon@sktelecom.com"], 'SM-N971N', 'SM-N976N', 'SM-A908N', 'SM-F907N'], ['SM-G981N', 'SM-G986N', 'SM-G988N']]
    model_list = [element for array in model_lists for element in array]

    model_list
    # In[3]:

    import os
    from datetime import datetime, timedelta
    from dateutil.parser import parse
    import time

    # directory = "./SS_FOTA_FTP"
    # os.chdir(directory)

    print(os.getcwd())

    # In[4]:

    if not os.path.exists(os.path.join(os.getcwd(), "data")):
        os.makedirs(os.path.join(os.getcwd(), "data"))

    # if not os.path.exists(os.path.join(os.getcwd(), "data", dt)):
    #     os.makedirs(os.path.join(os.getcwd(), "data", dt))

    # In[5]:

    def getCurrentDate(t=3):
        dayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
        dt = datetime.now()

        if t == 1:
            return dt.strftime("%A %d. %B %Y %H:%M:%S")
        elif t == 2:
            return dt.strftime("%Y%m%d") + "(" + dayOfWeek[dt.weekday()] + ")"
        elif t == 3:
            return dt.strftime("%Y%m%d")
        elif t == 4:
            return dt.strftime("%m%d")
        elif t == 5:
            return dt.strftime("%Y%m%d") + "_" + dayOfWeek[dt.weekday()] + "_" + dt.strftime("%H%M%S")

    def getshiftday(day1, dayshift):
        date = parse(day1) + timedelta(days=dayshift)
        return date.strftime("%Y%m%d")

    def getWeeksetAndNextStartDay(d1, d2):
        if parse(d2) < parse(getshiftday(d1, 6)):
            return [d1, d2], getshiftday(d2, 1)
        return [d1, getshiftday(d1, 6)], getshiftday(d1, 7)("%Y%m%d"), -1

    today = getCurrentDate()
    yesterday = getshiftday(today, -1)

    print(today, yesterday)

    # In[6]:

    # # FTP에서 File load
    # # SS FOTA 서버로 부터 크롤링 -> FTP 업로드 된 파일 다운로드
    # import ftplib
    # import os
    # from datetime import datetime, timedelta
    # from dateutil.parser import parse
    # import time

    # #오늘 날짜의 8시 Data 파일만 리턴
    # def syncfile(file_list):
    #     sel_file = []

    #     print(file_list)

    #     for f in file_list:
    #         if ("ss_fota_current_" in f) or ("ss_fota_last90days_" in f) :
    #             date = f.split("_")[3].split(".")[0]
    # #             time = f.split("_")[4].split(".")[0]
    # #             print(f, date, time)

    #             if(date == today) or (date == yesterday): # and ("080" in time)):
    #                 print("select :" + f)
    #                 sel_file.append(f)
    #     return sel_file

    # # filename = ["ss_fota_last90days.csv", "ss_fota_current.csv"]
    # filename = []
    # ftp=ftplib.FTP()
    # ftp.connect("223.62.224.35",21)
    # ftp.login("iotinfo","sktdatainfo#1231")
    # # ftp.cwd("/")

    # file_list = syncfile(ftp.nlst())
    # down_list = filename + file_list

    # print(down_list)

    # for f in down_list:
    #     date = f.split("_")[3]
    #     date = date.split(".")[0]
    # #     time = f.split("_")[4].split(".")[0]

    #     folder = "data/" + date
    #     if not os.path.exists(os.path.join(os.getcwd(), folder)):
    #         os.makedirs(os.path.join(os.getcwd(), folder))
    #         print("create dir : " + os.path.join(os.getcwd(), folder))

    #     fd = open(folder +  "/" + f,'wb')
    #     ftp.retrbinary("RETR " + f, fd.write)

    # fd.close()

    # In[7]:

    # max(["data/"+ f for f in os.listdir("data/") if not "." in f])
    # os.listdir("data/")
    sorted(["data/" + f for f in os.listdir("data/") if not "." in f])[0]
    list(reversed(["data/" + f for f in os.listdir("data") if not "." in f]))[0]

    # In[8]:

    def file_select(id=1, day=None):

        if id == 1:
            key = "ss_fota_last90day"
        elif id == 2:
            key = "ss_fota_current"

        lastdir = list(reversed(["data/" + f for f in os.listdir("data") if not "." in f]))[0]  # 최근 폴더
        if (day == "yesterday"):
            lastdir = list(reversed(["data/" + f for f in os.listdir("data") if not "." in f]))[1]  # 2번째 최근 폴더(하루 전 가정)

        lastdate = sorted([lastdir + "/" + f for f in os.listdir(lastdir) if key in f])[
            0]  ##가장 먼저 연동한 Data, 오전 8시에 근접할 가능성 높으니까..
        print(lastdate)
        return lastdate

    file_select(2)
    file_select(2, "yesterday")

    # data/20200108/

    # In[35]:

    # 최근 시점(Data Sync 시점) 업그레이드 가입자 현황
    # ss_fota_current = pd.read_csv("data/" + file_list[0] ,encoding='euc-kr')
    lastdir = list(reversed(["data/" + f for f in os.listdir("data") if not "." in f]))[0]
    ss_fota_current = pd.read_csv(file_select(2, today), encoding='euc-kr')  # for Test
    ss_fota_current_d1 = pd.read_csv(file_select(2, "yesterday"), encoding='euc-kr')  # for Test

    # 일자별 업그레이드 가입자 현황 (90일)
    ss_fota_lastday = pd.read_csv(file_select(1, today), encoding='euc-kr')

    ss_fota_current.rename(columns={'ap_cp': 'AP_CP'}, inplace=True)
    ss_fota_current_d1.rename(columns={'ap_cp': 'AP_CP'}, inplace=True)
    ss_fota_lastday.rename(columns={'ap_cp': 'AP_CP'}, inplace=True)

    # 삼성 FOTA 서버로 부터 Data Synk 시간
    sync_date = str(ss_fota_current["sync_dt"].unique()[0])
    sync_time = "{:>04d}".format(ss_fota_current["sync_time"].unique()[0])

    sync_date_d1 = str(ss_fota_current_d1["sync_dt"].unique()[0])
    sync_time_d1 = "{:>04d}".format(ss_fota_current_d1["sync_time"].unique()[0])

    print("============")
    # print("Fota Server Data Sync Time : {} {:>04d}".format(sync_date, sync_time))
    print("Fota Server Data Sync Time : {} {}".format(sync_date, sync_time))
    print("Fota Server Data Sync Time D-1 : {} {}".format(sync_date_d1, sync_time_d1))

    print("============")

    # In[ ]:

    # 교품 반품 보정
    g977_exchange = list()
    g977_exchange.append({"sw": "SD1_SD2", "value": 185})
    g977_exchange.append({"sw": "SD1_SD5", "value": 721})
    g977_exchange.append({"sw": "SD7_SD8", "value": 193})
    g977_exchange.append({"sw": "SD7_SDA", "value": 231})
    g977_exchange.append({"sw": "SDB_SDA", "value": 973})
    g977_exchange.append({"sw": "SE5_SE5", "value": 853})
    g977_exchange.append({"sw": "SE8_SE6", "value": 1484})

    def subtract_exchange_count(df, model, target, counts):
        totvalue = 0;
        for count in counts:
            df.loc[(df["Model"] == model) & (df["AP_CP"] == count["sw"]), target] = df.loc[(df["Model"] == model) & (
                        df["AP_CP"] == count["sw"]), target] - count["value"]
            totvalue += count["value"]

        df.loc[(df["Model"] == model), "Total Device Count"] = df.loc[(df[
                                                                           "Model"] == model), "Total Device Count"] - totvalue
        df.loc[(df["Model"] == model), "MS"] = df.loc[(df["Model"] == model), target] / df.loc[
            (df["Model"] == model), "Total Device Count"] * 100
        return df

    ss_fota_current = subtract_exchange_count(ss_fota_current, "SM-G977N", "Total Count", g977_exchange)
    ss_fota_current_d1 = subtract_exchange_count(ss_fota_current_d1, "SM-G977N", "Total Count", g977_exchange)
    ss_fota_lastday = subtract_exchange_count(ss_fota_lastday, "SM-G977N", "Device Count", g977_exchange)

    # In[37]:

    # 레이블 설정 형식 : ap_cp(FOTA Open 날짜)
    ss_fota_lastday['Lable'] = ss_fota_lastday['AP_CP'] + "(" + ss_fota_lastday['First Open Date'] + ")"

    # Datatiem 형식으로 변경
    ss_fota_lastday['Date'] = pd.to_datetime(ss_fota_lastday['Date'], format='%Y-%m-%d')

    ss_fota_lastday = ss_fota_lastday.loc[ss_fota_lastday['release_sw'].notnull()]  # 예외 모델 제거

    # 삼성 포타 모델 정보
    ss_fota_info = ss_fota_lastday[
        ['Model Group', 'pet_name', 'Model', 'AP_CP', 'ua_ver', 'OS Version', 'Last Version', 'First Open Date',
         'Firmware Size (MB)', 'Security Patch Version', 'release_type', 'ue_type']].drop_duplicates(
        ['Model', 'AP_CP', 'ua_ver'], keep='last')

    fname = lastdir + "/ss_fota_info_" + str(sync_date) + ".csv"
    ss_fota_info.to_csv(fname, encoding='euc-kr', index=False)

    ss_fota_lastday.head()

    # In[15]:

    # ss_fota_lastday

    # In[39]:

    # realtime 결과 report 형식으로 변환
    def conver_report_foramt_current(ss_fota_current, ss_fota_info):
        # Datatiem 형식으로 변경
        ss_fota_current['sync_dt'] = ss_fota_current['sync_dt'].astype(str)
        ss_fota_current['sync_time'] = ss_fota_current['sync_time'].astype(str)

        # 최근 가입자 현황 + 모델 정보 통합
        df1 = ss_fota_current.loc[
            ss_fota_current['release_sw'].notnull(), ['Model', 'AP_CP', 'Total Count', 'MS', 'Total Device Count',
                                                      'ua_ver', 'release_sw', 'sync_dt', 'sync_time']]
        df1.rename(columns={'Total Count': 'Count'}, inplace=True)
        df1.rename(columns={'Total Device Count': 'Total Count'}, inplace=True)
        df1.rename(columns={'MS': 'MS(%)'}, inplace=True)

        df2 = ss_fota_info
        ss_fota_recent = pd.merge(df1, df2, how='outer')

        #     print(ss_fota_recent.head())
        return ss_fota_recent

    # 최근 Data
    ss_fota_recent = conver_report_foramt_current(ss_fota_current, ss_fota_info)

    # 하루전 Data와 통합
    ss_fota_recent_d1 = conver_report_foramt_current(ss_fota_current_d1, ss_fota_info)[
        ["Model", "AP_CP", "Count", "Total Count", "sync_dt", "sync_time"]]
    ss_fota_recent_d1.rename(columns={'Count': 'Count_D-1', 'Total Count': 'Total Count_D-1', 'sync_dt': 'sync_dt_D-1',
                                      'sync_time': 'sync_time_D-1'}, inplace=True)
    ss_fota_recent = pd.merge(ss_fota_recent, ss_fota_recent_d1, on=['Model', 'AP_CP'], how='left')
    ss_fota_recent["Delta Count"] = ss_fota_recent["Count"] - ss_fota_recent["Count_D-1"]
    ss_fota_recent["Delta Total Count"] = ss_fota_recent["Total Count"] - ss_fota_recent["Total Count_D-1"]

    ss_fota_recent["MS(%)"] = ss_fota_recent["MS(%)"].round(2)

    coun_list = [p for p in ss_fota_recent.columns if "Count" in p]
    ss_fota_recent[coun_list] = ss_fota_recent[coun_list].fillna(0.0).astype(int)  # int type 변환

    ss_fota_recent_fname = lastdir + "/ss_fota_DeviceCount_" + str(sync_date) + "_" + str(sync_time) + ".csv"
    ss_fota_recent.to_csv(ss_fota_recent_fname, encoding='euc-kr', index=False)

    # 첨부파일
    ss_fota_recent_attach = ss_fota_recent[
        ['Model', 'ua_ver', 'release_sw', 'Model Group', 'OS Version', 'Last Version', 'First Open Date',
         'Firmware Size (MB)', 'Security Patch Version', 'release_type', 'ue_type']]
    ss_fota_attach_fname = lastdir + "/ss_fota_attachment_" + str(sync_date) + "_" + str(sync_time) + ".csv"
    ss_fota_recent_attach.to_csv(ss_fota_attach_fname, encoding='euc-kr', index=False)

    ss_fota_raw_current_fname = lastdir + "/ss_fota_real_time_" + str(sync_date) + "_" + str(sync_time) + ".xlsx"

    print(ss_fota_attach_fname)
    print(ss_fota_recent_attach.columns)


    # # 모델별 최근 가입자 현황 출력

    # In[40]:

    # from IPython.display import display, HTML
    # for modle in model_list:
    #     pte_name = ss_fota_recent['pet_name'].unique()[0]
    #     data = ss_fota_recent.loc[ss_fota_recent['Model'] == modle , ['Model','ap_cp','Count','MS(%)','Total Device Count','ua_ver','Model Group', 'pet_name','OS Version','Last Version','First Open Date','Firmware Size (MB)','Security Patch Version','release_type','ue_type','sync_dt','sync_time']].reset_index()
    #     print("< {}({}) >".format(pte_name, modle))
    #     display(HTML(data.to_html()))
    #     print("SUM {} / {}%".format(data["Count"].sum(), data["MS(%)"].sum()))
    #     print("========================================\n")

    # # 일별 그래프(24시 기준 Data) 및 표(최근 연동시점) 출력

    # In[41]:

    # get_ipython().run_line_magic('matplotlib', 'inline')
    import matplotlib.pyplot as plt
    from datetime import datetime
    import matplotlib.dates as mdates
    import matplotlib as mpl
    # from IPython.display import display, HTML

    # pd.options.display.float_format = '{:20,.2f}'.format

    # model_list = ['SM-G977N']
    marker = [".", "o", "v", "^", "<", ">", "1", "2", "3", "4", "s", "p", "*", "h", "H", "+", "x", "D", "d"]

    for model in model_list:
        data = ss_fota_lastday.loc[(ss_fota_lastday["Model"] == model)]
        index = "Lable"
        x_column = 'Date'
        aggfunc = 'sum'
        values = 'Device Count'
        pte_name = data['pet_name'].unique()[0]

        pivot_tabile = pd.pivot_table(data=data, index=index, columns=x_column, aggfunc=aggfunc, values=values).T
        pivot_tabile['Total'] = pivot_tabile.sum(axis=1)

        fig = plt.figure(figsize=(20, 6))
        ax = fig.add_subplot(1, 1, 1)
        plt.title(pte_name + "(" + model + ")", fontsize=20)

        mk_index = 0
        for sw in pivot_tabile.columns:

            if (sw == 'Total'):
                plt.plot(pivot_tabile[sw], ls=":", color='gray', marker="", label=sw)
            else:
                plt.plot(pivot_tabile[sw], '-', marker=marker[mk_index], markersize=4, label=sw)

            #         plt.axvline(x=datetime(2019,12,17), color='r', linestyle='--', linewidth=2)   #세로줄
            mk_index = (mk_index + 1) % (len(marker) - 1)

        plt.legend(loc=7, fontsize= 13, bbox_to_anchor=(1.16, 0.5))

        # Grop 설정
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=1)

        plt.xticks(rotation=45, fontsize= 12.3)

        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        fig.patch.set_facecolor('xkcd:white')
        # plt.show()
        fig.savefig(model + ".png", bbox_inches='tight') # Use fig. here

        # 표출력, 마지막 연동 시점 기준
        df = ss_fota_recent.loc[ss_fota_recent['Model'] == model]
        df = df[['Model', 'AP_CP', 'Count', 'MS(%)', 'Total Count', 'Delta Count', 'Delta Total Count', 'ua_ver',
                 'Model Group', 'pet_name', 'OS Version', 'Last Version', 'First Open Date', 'Firmware Size (MB)',
                 'Security Patch Version', 'release_sw', 'release_type', 'ue_type', 'sync_dt',
                 'sync_time']].reset_index()
        print("< {}({}) : {}기준>".format(pte_name, model, str(sync_date) + "_" + str(sync_time)))
        # display(HTML(df.to_html()))
        # print("SUM {} / {}%".format(df["Count"].sum(), df["MS(%)"].sum()))
        print("========================================\n")

    # In[42]:

    print("END")
    ss_fota_recent.loc[ss_fota_recent['Model'] == model].head()

    # In[43]:

    import os

    # directory = "./SS_FOTA_FTP"
    # os.chdir(directory)

    print(os.getcwd())

    # # 메일전송

    # In[44]:

    from email.mime.image import MIMEImage
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    from os.path import basename

    class MailSender(object):
        def __init__(self, username, password, server='smtp.gmail.com', port=587, use_tls=True):
            self.username = username
            self.password = password
            self.server = server
            self.port = port
            self.use_tls = use_tls

        def send(self, sender, recipients, subject, message_plain='', message_html='', images=None, files=None):
            '''

            :param sender: str
            :param recipients: [str]
            :param subject: str
            :param message_plain: str
            :param message_html: str
            :param images: [{id:str, path:str}]
            :return: None
            '''

            msg_related = MIMEMultipart('related')

            msg_related['Subject'] = subject
            msg_related['From'] = sender
            msg_related['To'] = ', '.join(recipients)
            msg_related.preamble = 'Please check e-mail file.'

            msg_alternative = MIMEMultipart('alternative')
            msg_related.attach(msg_alternative)

            plain_part = MIMEText(message_plain, 'plain')
            html_part = MIMEText(message_html, 'html')

            msg_alternative.attach(plain_part)
            msg_alternative.attach(html_part)

            if images:
                for image in images:
                    with open(image['path'], 'rb') as f:
                        msg_image = MIMEImage(f.read())
                        msg_image.add_header('Content-ID', '<{0}>'.format(image['id']))
                        msg_related.attach(msg_image)

            # Sending the mail

            if files:
                for f in files or []:
                    with open(f, "rb") as fil:
                        part = MIMEApplication(fil.read(), Name=basename(f))
                    # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                    msg_related.attach(part)

            server = smtplib.SMTP('{0}:{1}'.format(self.server, self.port))
            try:
                if self.use_tls:
                    server.starttls()

                server.login(self.username, self.password)
                server.sendmail(sender, recipients, msg_related.as_string())
            #             print(msg_related.as_string())

            finally:
                server.quit()
    # In[45]:

    import os

    # directory = "./SS_FOTA_FTP"
    # os.chdir(directory)

    print(os.getcwd())

    # In[49]:

    # ! /usr/bin/python
    # -*- coding: utf-8 -*-
    # from mailsender import MailSender

    from tabulate import tabulate
    from premailer import transform

    def highlight_max(s):
        '''
        highlight the maximum in a Series yellow.
        '''
        is_max = s == s.max()
        retval = ['background-color: #ECEBEB' if v else '' for v in is_max]
        return retval

    styles = [
        dict(selector="th", props=[("font-size", "85%"),
                                   ("text-align", "center")])
    ]

    from connection_info import get_connection_info

    smtp_host = get_connection_info("gmail_smtp_host")
    username = get_connection_info("gmail_user")
    password = get_connection_info("gmail_pw")

    sender = username

    images = list()
    files = list()

    html_more = """
        <tr>
            <td align="center">
            <p><H1>[model]</H1></p>
            </td>
        </tr>
        <tr>
            <td width="100%" valign="top" bgcolor="d0d0d0" style="padding:5px;">              
            <img width="100%" height="100%" src="cid:[imgname_id]" />
            </td>
        </tr>
        <tr>
            <td width="1000" align="center" valign="top" bgcolor="white" style="padding:5px;border:2px solid #444444">
            {table1}        
        </tr>
        <tr>
            <td width="1000" align="center" valign="top" bgcolor="white" style="padding:5px;border:2px solid #444444">
            <p><H3>[total_data]</H3></p>
        </tr>
        <tr><td align="center"><p><H3> </H3></p></td></tr>


        {more}

    """

    page = 0
    total_page = len(model_lists)
    for models in model_lists:
        page += 1
        print(page, models)
        with open('template.html', encoding='UTF-8') as template_html, open('template.txt') as template_plain:
            message_html = template_html.read()
            message_plain = template_plain.read()

            message_html = message_html.format(Date="Data Sync Time : {} {}".format(sync_date, sync_time),
                                               Date_d1="Delta Sync Time : {} {}".format(sync_date_d1, sync_time_d1),
                                               more="{more}")


            for model in models:
                df = ss_fota_recent.loc[ss_fota_recent['Model'] == model]
                pte_name = df["pet_name"].unique()[0]
                #         df = df[['pet_name', 'Model','AP_CP','Count','MS(%)','Total Count', 'Delta Count', 'Delta Total Count', 'ua_ver', 'OS Version','Last Version','First Open Date','Firmware Size (MB)','release_type','ue_type']].reset_index().drop("index", axis=1)
                df_print = df[['First Open Date', 'AP_CP', 'ua_ver', 'Count', 'MS(%)', 'Delta Count', 'OS Version',
                               'Firmware Size (MB)']].reset_index().drop("index", axis=1)

                html_add = html_more.replace("[imgname_id]", "img_" + model)
                html_add = html_add.replace("[model]", pte_name + "(" + model + ")")

                total = df['Total Count'].unique()[0]
                total_delta = df['Delta Total Count'].unique()[0]
                sign = "+"
                if (total_delta < 0):
                    sign = ""
                html_add = html_add.replace("[total_data]",
                                            'Total Count : {:,} ( {}{:,} )'.format(total, sign, total_delta))

                images.append({'id': "img_" + model, 'path': model + ".png"})

                # col_list = list(df_print.columns.values)
                # message_html = message_html.format(more=html_add)
                # message_html = message_html.format(table1=tabulate(df_print, headers=col_list, tablefmt="html"),
                #                                    more="{more}")

                message_html = message_html.replace('{more}', html_add)

                s = df_print.style.format({'Count': "{:,}", 'Delta Count': '{:+,}', 'MS(%)': '{:.2f}', 'Delta MS(%)': '{:+.2f}'}) \
                    .set_properties(**{'text-align': 'right', 'padding' : "2px", 'border':'1px', 'border-style' :'solid', 'border-color':'#DFDEDE'}) \
                    .apply(highlight_max, subset=['Count', 'MS(%)', 'Delta Count']) \
                    .set_table_styles(styles)

                message_html = message_html.replace('{table1}', transform(s.render()))   #teams 공유를 위해 transform로 inline style로 변경 필요

            message_html = message_html.format(more="")

            print("images : ", images)

            if (page == total_page):  # 마지막 메일에 파일 첨부
                files.append(ss_fota_recent_fname)
                files.append(ss_fota_raw_current_fname)
                print("files: ", files)

            mail_sender = MailSender(username, password, server=smtp_host)


            if __name__ == "__main__":
                # 테스트 메일 #Jupyter 노트 북 또는 개별 모듈 실행시
                print("테스트 메일")
                mail_sender.send(sender, email_list,
                                 '삼성 FOTA 연동 현황_Custom ({}/{})'.format(page, total_page), message_html=message_html, message_plain=message_plain, images=images, files=files)
            else :
                # Teams 공유 메일 주소
                mail_sender.send(sender, email_list,
                                 '삼성 FOTA 연동 현황_Custom ({}/{})'.format(page, total_page), message_html=message_html, message_plain=message_plain, images=images,
                                 files=files)

        print("complet!!")

## Start
if __name__ == "__main__":
    start_send_report_email_custom([['SM-G970N', 'SM-G973N', 'SM-G975N', 'SM-G960N', 'SM-G965N','SM-G950N','SM-G955N','SM-N960N','SM-N950N', 'SM-G986N-BTS']], ["58fc60be.o365skt.onmicrosoft.com@apac.teams.ms", "sukchan.jung@sktelecom.com", "jungil.kwon@sktelecom.com"])


