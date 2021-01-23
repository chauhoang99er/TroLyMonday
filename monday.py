import os
import playsound
import wikipedia
import speech_recognition
import time
import datetime
import webbrowser
import re
from youtube_search import YoutubeSearch
import pyttsx3

#Thiết lập từ điển Tiếng Việt
wikipedia.set_lang('vi')
language = 'vi'

#---------Speaking---------
def monday_speaking(audio):
    print("MONDAY:",audio)
    monday = pyttsx3.init()
    monday_voice = monday.getProperty('voices')
    rate = monday.getProperty('rate')
    volume = monday.getProperty('volume')
    monday.setProperty('volume', volume - 0.0)
    monday.setProperty('rate', rate - 50)
    monday.setProperty('voice', monday_voice[1].id)
    monday.say(audio)
    monday.runAndWait()

def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 5 and hour < 12:
        monday_speaking("Chào Buổi Sáng")
    elif hour >= 12 and hour < 18:
        monday_speaking("Chào Buổi Chiều")
    elif hour >= 18 and hour < 24:
        monday_speaking("Chào Buổi Tối")

#---------Listening---------
def monday_listening():
    monday_ear = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        print("MONDAY: Tôi Đang Nghe....")
        audio = monday_ear.listen(mic, phrase_time_limit= 6) #mls
        try:
            you = monday_ear.recognize_google(audio, language="vi-VN")
            print("Bạn:",you)
            return you
        except:
            print("Lỗi rồi tôi không nghe được !!!")
            return 0

#---------Lặp Lệnh---------
def monday_request():
    for i in range(3):
        request = monday_listening()
        if request:
            return request.lower()
        elif i < 2:
            monday_speaking("Vui lòng nói lại !!!")
    time.sleep(3)
    monday_speaking("Tạm biệt bạn !!!")
    return 0

#---------Xem Thời Gian---------
def get_time(monday_brain):
    now = datetime.datetime.now()
    if 'giờ' in monday_brain:
        monday_speaking(f"Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây")
    elif 'ngày' in monday_brain:
        monday_speaking(f"Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}")     

#---------Mở Ứng Dụng---------
def open_App(monday_brain):
    if "cốc cốc" in monday_brain:
        monday_speaking("Mở Ứng Dụng Cốc Cốc")
        os.system("C:\\Users\\Admin\\Documents\\App\\CocCoc.lnk")
    elif 'chrome' in monday_brain:
        monday_speaking("Mở Ứng Dụng Google Chrome")
        os.system("C:\\Users\\Admin\\Documents\\App\\GoogleChrome.lnk")
    elif 'word' in monday_brain:
        monday_speaking("Mở Ứng Dụng Word")
        os.system("C:\\Users\\Admin\\Documents\\App\\Word.lnk")
    elif 'excel' in monday_brain:
        monday_speaking("Mở Ứng Dụng Excel")
        os.system("C:\\Users\\Admin\\Documents\\App\\Excel.lnk")
    else:
        monday_speaking("Chưa hỗ trợ ứng dụng này !!!")

#---------Mở Trang Web---------
def open_Website(monday_brain):
    monday_speaking("Bạn cần tôi mở trang web nào?")
    search_web = monday_listening().lower()
    op_Web = re.search('trang web (.+)',search_web)
    if op_Web:
        domain = op_Web.group(1)  
        url = "https://www." + domain
        webbrowser.open(url)
        monday_speaking("Trang web bạn yêu cầu đã được mở")
        return True
    else: return False 

#---------Search_Google---------
def google_search(monday_brain):
    monday_speaking("Bạn cần tôi tìm kiếm thứ gì?")
    search = monday_listening().lower()
    if search:
        url = f"https://www.google.com/search?q={search}"
        webbrowser.get().open(url)
        monday_speaking(f'Đây là kết quả của từ khóa {search} trên Google')
        if input("Để trợ lý ảo tiếp tục vui lòng nhấn n: ") == "n":
            pass
        return True
    else:
        return False

#---------Search_Youtube---------
def youtube_search(monday_brain):
    monday_speaking("Bạn cần tôi tìm kiếm thứ gì trên Youtube?")
    search = monday_listening().lower()
    if search:
        url = f"https://www.youtube.com/search?q={search}"
        webbrowser.get().open(url)
        monday_speaking(f'Đây là kết quả của từ khóa {search} trên Youtube')
    else:
        return False
    #Xem Video Đầu Tiên
    monday_speaking('Bạn có muốn xem video đầu tiên không?')
    open_first = monday_listening()
    if "có" in open_first:
        while True:
            result = YoutubeSearch(search, max_results= 10).to_dict()   
            if result:
                break
        url_ytb = f"https://www.youtube.com" + result[0]['url_suffix']    
        webbrowser.get().open(url_ytb) 
        monday_speaking('Đây là video của bạn')
        if input("Để trợ lý ảo tiếp tục vui lòng nhấn n: ") == "n":
            pass
        return True
    else: 
        if input("Để trợ lý ảo tiếp tục vui lòng nhấn n: ") == "n":
            pass
        return True

#---------Knowledge---------
def monday_knowledge():
    welcome()
    monday_speaking("Bạn tên là gì?")
    name_user = monday_request()
    if name_user:
        monday_speaking(f'Xin chào {name_user}')
        monday_speaking(f'Tôi có thể giúp gì cho bạn ?')
        while True:
            monday_brain = monday_request()

            if not monday_brain:
                break
            elif ("hiện tại" in monday_brain) or ("hôm nay" in monday_brain):
                get_time(monday_brain)
            elif ("mở ứng dụng" in monday_brain):
                open_App(monday_brain)
            elif ("mở trang web" in monday_brain):
                open_Website(monday_brain)
            elif ("tìm kiếm" in monday_brain):
                if ("youtube" in monday_brain):
                    youtube_search(monday_brain)
                else:
                    google_search(monday_brain)
            elif ("tạm biệt" in monday_brain):
                monday_speaking(f'Tạm biệt {name_user}')
                break
            else:
                monday_speaking("Tôi không hiểu, vui lòng nói lại !!!")

monday_knowledge()