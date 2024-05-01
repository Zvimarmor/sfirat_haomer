from bidi.algorithm import get_display
from astral.sun import sun
from astral import LocationInfo
import pywhatkit as pywhatkit
import datetime
import time

sfirot = ["חסד", "גבורה", "תפארת", "נצח", "הוד", "יסוד", "מלכות"]
lel_haseder_date = datetime.datetime(2024, 4, 23)

def get_sunset_time(location = "Jerusalem"):
    location = LocationInfo(location, "Israel", "Asia/Jerusalem", "31.768318", "35.213711")
    today = datetime.datetime.now()
    s = sun(location.observer, date=today)
    sunset_time = s['sunset'] + datetime.timedelta(hours=3)
    return sunset_time

def what_day_is_it(location = "Jerusalem"):
    now = datetime.datetime.now()
    sunset_time = get_sunset_time(location)

    if now.hour < sunset_time.hour or (now.hour == sunset_time.hour and now.minute < sunset_time.minute):
        answer = now - lel_haseder_date
    else:
        answer = now - lel_haseder_date + datetime.timedelta(days=1)

    answer = answer.days
    if answer < 1:
        return "Invalid day"
    elif answer > 49:
        return "Invalid day"
    return answer
    
def what_sfira_is_it(day):
        if day < 1 or day > 49:
            return "Invalid day"
        week = (day - 1) // 7
        day_in_week = (day - 1) % 7
        return (sfirot[day_in_week], sfirot[week])

class sfirat_haomer:
    def __init__(self, day) -> None:
        self.day = int(day)
        self.sfira = what_sfira_is_it(day)
    
    def __str__(self) -> str:
        return get_display("היום " + str(self.day) + " ימים לעומר. הספירה של היום היא " + self.sfira[0] + " שב" + self.sfira[1])

def return_sfirat_haomer_from_user():
    day = int(input(get_display("הכנס את יום ספירת העומר: ")))
    while day < 1 or day > 49:
        if day < 1:
            print(get_display("אופס! עדיין לא מחרת השבת!") + "\n")
            day = int(input(get_display("הכנס את יום ספירת העומר: ")))
        elif day > 49:
            print(get_display("אופס! כבר נגמרה ספירת העומר השנה!") + "\n")
            day = int(input(get_display("הכנס את יום ספירת העומר: ")))
    today = sfirat_haomer(day)
    print(today)

def build_message_for_user(today, Nosach = "Sfard"):
    message = get_display("היי! זהו תזכורת לספירת העומר היומית שלך!" + "\n" + "\n")
    message += get_display("ברוך אתה ה' אלוהינו מלך העולם, אשר קדשנו במצוותיו וציוונו על ספירת העומר." + "\n")
    message += str(sfirat_haomer(today)) + "\n"
    return message

def send_Whatsapp_messege(message, phone_number):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1
    print("the message will be sent at: " + str(hours) + ":" + str(minutes))
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes+1)
    return

def get_phone_number():
    phone_number = input(get_display("מה מספר הפלאפון שלך לשליחת התזכורת?"))
    if phone_number[0] != "0" or phone_number[1] != "5":
        input(get_display("המספר שהכנסת אינו תקין. אנא הכנס מספר פלאפון תקין."))
    if len(phone_number) != 10:
        input(get_display("המספר שהכנסת אינו תקין. אנא הכנס מספר פלאפון תקין."))
    return phone_number

def get_Nosach():
    Nosach = input(get_display("מה נוסח התפילה שלך?"))
    if Nosach not in ["אשכנז", "ספרד", "עדות המזרח"]:
        input(get_display("הנוסח שהכנסת אינו תקין. אנא הכנס נוסח תקין."))
    if Nosach == "":
        Nosach = "Sfard"
    if Nosach == "אשכנז":
        Nosach = "Ashkenaz"
    if Nosach == "ספרד":
        Nosach = "Sfard"
    if Nosach == "עדות המזרח":
        Nosach = "Edot Hamizrach"
    return Nosach

def get_location():
    location = input(get_display("מה מקום מגוריך?"))
    if location == "":
        location = "Jerusalem"
    if location == "ירושלים":
        location = "Jerusalem"
    if location == "תל אביב":
        location = "Tel Aviv"
    if location == "חיפה":
        location = "Haifa"
    if location == "באר שבע":
        location = "Beer Sheva"
    return location

def main():
    user_phone_number = get_phone_number()
    user_Nosach = get_Nosach()
    user_location = get_location()
    today = what_day_is_it(user_location)
    message = build_message_for_user(today, user_Nosach)
    while today <= 49:
        today = what_day_is_it(user_location)
        message = build_message_for_user(today, user_Nosach)
        send_Whatsapp_messege(get_display(message), user_phone_number)
        time.sleep(24*60*60)
    print(get_display("סיימתי לשלוח תזכורות!"))
    return
    
if __name__ == "__main__":
    main()  


