from bidi.algorithm import get_display
import pywhatkit as pywhatkit
import datetime
import time

sfirot = ["חסד", "גבורה", "תפארת", "נצח", "הוד", "יסוד", "מלכות"]
sfirots = ["chesed", "gevurah", "tiferet", "netzach", "hod", "yesod", "malchut"]
lel_haseder_date = datetime.datetime(2024, 4, 23)

def what_day_is_it():
    now = datetime.datetime.now()
    answer = now - lel_haseder_date
    if answer.days < 1:
        return "Invalid day"
    elif answer.days > 49:
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
        self.day = day
        self.sfira = what_sfira_is_it(day)
    
    def __str__(self) -> str:
        return get_display("ספירת העומר היום היא " + str(self.day) + " לעומר, שהיא " + self.sfira[0] + " שב" + self.sfira[1])

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
    message = get_display("היי! זהו תזכורת לספירת העומר היומית שלך!" + "\n")
    message += get_display("ברוך אתה ה' אלוהינו מלך העולם, אשר קדשנו במצוותיו וציוונו על ספירת העומר. יום ה" + "\n")
    message += str(sfirat_haomer(today)) + "\n"
    return message


def send_Whatsapp_messege(message, phone_number = "+972534600460"):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1
    print("the message will be sent at: " + str(hours) + ":" + str(minutes))
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes+1)

def main():
    user_phone_number = input(get_display("מה מספר הפלאפון שלך לשליחת התזכורת( כולל קידומת מדינה)?"))
    user_Nosach = input(get_display("מה נוסח התפילה שלך?"))
    today = what_day_is_it().days
    message = build_message_for_user(today, user_Nosach)
    while today <= 49:
        today = what_day_is_it().days
        message = build_message_for_user(today, user_Nosach)
        send_Whatsapp_messege(message, user_phone_number)
        time.sleep(24*60*60)
    

if __name__ == "__main__":
    main()
    


