from bidi.algorithm import get_display
import pywhatkit as pywhatkit
import datetime

sfirot = ["חסד", "גבורה", "תפארת", "נצח", "הוד", "יסוד", "מלכות"]
sfirots = ["chesed", "gevurah", "tiferet", "netzach", "hod", "yesod", "malchut"]
lel_haseder_date = datetime.datetime(2024, 4, 23)

def what_day_is_it():
    now = datetime.datetime.now()
    return now - lel_haseder_date
    

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

def send_Whatsapp_messege(message):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1
    pywhatkit.sendwhatmsg("+972534600460", message, hours, minutes+1)
    


if __name__ == "__main__":
    today = sfirat_haomer(what_day_is_it().days)
    message = get_display(str(today))
    send_Whatsapp_messege(message)
    

