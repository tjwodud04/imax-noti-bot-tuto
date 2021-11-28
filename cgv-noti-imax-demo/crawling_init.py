import datetime
import requests
import telegram

from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

def check_imax():
    # CGV 메인 도메인 + 예매시간표 페이지 iframe 내 자원주소(src)
    url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0074&screencodes=&screenratingcode=02&regioncode=07"
    today = datetime.date.today().strftime("%Y%m%d")
    url += today

    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')

    chatbot = telegram.Bot(token = 'telegram-personal-token')


    # 타겟: 해당 날짜에 상영중인 영화 목록 하나씩 출력 + <strong> 태그 떼고 출력
    result = []

    # 이상한 값이 끼어들어와서 이후에 replace로 날려줄 값
    nullvalue = '[<strong>\r\n                                                '
    nullvalue2 = '</strong>]'

    # 상영목록이 담긴 리스트를 받아옴
    timetable = bs.find_all('div', attrs={"class": "col-times"})

    if (timetable):
        for i in timetable:
            title = i.select('a > strong')
            result.append(str(title))

        result = [word.replace(nullvalue, '') for word in result]
        result = [word.replace(nullvalue2, '') for word in result]

        for movie in result:
            chatbot.sendMessage(chat_id= telegram-id-number, text = movie + "의 왕십리 IMAX관 예매가 오픈되었습니다.")
            # 오픈된 경우 더이상의 수행 및 메시지 발송을 막음
            sc.pause()

    else:
        chatbot.sendMessage(chat_id= telegram-id-number, text = "아직 오픈된 왕십리 IMAX관 예매가 없습니다.")


# 스케쥴 구성을 위한 수행부
# check_imax()
sc = BlockingScheduler()
sc.add_job(check_imax, 'interval', seconds = 1800)
sc.start()
