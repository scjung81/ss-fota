import ftplib
import os

# from sendSMS import *
from sendMail import *
# sendMail(title="ss_fota started ", text="")

def ftpupload_file(dir, filename):

    # filename = "OSU1.png"
    ftp = ftplib.FTP()
    ftp.connect("223.62.224.35", 21)    #Ftp 주소 Connect(주소 , 포트)
    ftp.login("iotinfo", "sktdatainfo@0810")         #login (ID, Password)
    ftp.cwd("/home/iotinfo")   #파일 전송할 Ftp 주소 (받을 주소)

    current_dir = os.getcwd()

    #기존 파일 삭제
    for something in ftp.nlst():
        # print("key:", filename.split(".")[0]+"_")
        # if filename.split(".")[0]+"_" in something:
        if filename == something:
            print("Delete old file:", something)
            ftp.delete(something)

    os.chdir(dir) #파일 전송 대상의 주소(보내는 주소)
    # print(os.getcwd())
    myfile = open(filename, 'rb')       #Open( ~ ,'r') <= Text파일은 됨, Open( ~ ,'rb') <= 이미지파일 됨
    ftp.storbinary('STOR ' + filename, myfile)

    myfile.close()
    ftp.close()

    os.chdir(current_dir)
    # ftp://223.62.224.35/home
    # C:\Users\SKTelecom\PycharmProjects\PLM_Crawling\crawling\OSU1.png

def start_upload():
 #마지막 폴더 찾기
    filepath = "data"
    lastdate = max([filepath +"/"+ f for f in os.listdir(filepath)], key=os.path.getctime)
    abspath = os.path.dirname(os.path.abspath(__file__)) + "\/" + lastdate
    print(lastdate)

    file_list = os.listdir(lastdate)
    # print(file_list)

    update_list = []

    try :
        for file in file_list:
            #if file.find(".csv") != -1:
                print("upload ftp : " , file)
                ftpupload_file(abspath, file)
                update_list.append(file)

        print(update_list)
    except Exception as ex :
        print(ex)
        sendMail(title="ss_fota Error occurred, ftpupload_file ", text=ex.__str__())
        exit(-1)


    sendMail(title="ss_fota success file upload ", text="\n".join(update_list))

    return file_list


## Start
if __name__ == "__main__":
    start_upload()
