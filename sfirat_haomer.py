from bidi.algorithm import get_display
from astral.sun import sun
from astral import LocationInfo
import pywhatkit as pywhatkit
import datetime
import time

# List of Sefirot
sfirot = ["חסד", "גבורה", "תפארת", "נצח", "הוד", "יסוד", "מלכות"]

# Date of the first day of Passover
lel_haseder_date = datetime.datetime(2024, 4, 23)

# Function to get the time of sunset for a given location
def get_sunset_time(location = "Jerusalem"):
    # Create LocationInfo object
    location = LocationInfo(location, "Israel", "Asia/Jerusalem", "31.768318", "35.213711")
    # Get current date and time
    today = datetime.datetime.now()
    # Calculate sunset time
    s = sun(location.observer, date=today)
    sunset_time = s['sunset'] + datetime.timedelta(hours=3)  # Adjust for Israel timezone
    return sunset_time

# Function to determine the current day of the Omer
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

# Function to determine the corresponding Sefirah for a given day of the Omer
def what_sfira_is_it(day):
    if day < 1 or day > 49:
        return "Invalid day"
    week = (day - 1) // 7
    day_in_week = (day - 1) % 7
    return (sfirot[day_in_week], sfirot[week])

# Class representing a day of the Omer
class sfirat_haomer:
    def __init__(self, day) -> None:
        self.day = int(day)
        self.sfira = what_sfira_is_it(day)
    
    # Method to convert sfirat_haomer object to string
    def __str__(self) -> str:
        return get_display("היום " + str(self.day) + " ימים לעומר. הספירה של היום היא " + self.sfira[0] + " שב" + self.sfira[1])

# Function to prompt user for the current day of the Omer and return corresponding Sefirah
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

# Function to build message for user
def build_message_for_user(today, Nosach = "Sfard"):
    message = get_display("היי! זו היא תזכורת לספירת העומר היומית שלך!" + "\n" + "\n")
    message += get_display("ברוך אתה ה' אלוהינו מלך העולם, אשר קדשנו במצוותיו וציוונו על ספירת העומר." + "\n")
    message += str(sfirat_haomer(today)) + "\n"
    return message

# Function to send WhatsApp message
def send_Whatsapp_messege(message, phone_number):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1
    print("the message will be sent at: " + str(hours) + ":" + str(minutes))
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes+1)
    return

# Function to get user's phone number
def get_phone_number():
    while True:
        phone_number = input(get_display("מה מספר הפלאפון שלך לשליחת התזכורת?"))
        
        if phone_number[0] != "0" or phone_number[1] != "5":
            print(get_display("המספר שהכנסת אינו תקין. אנא הכנס מספר פלאפון תקין."))
            continue
        if len(phone_number) != 10:
            print(get_display("המספר שהכנסת אינו תקין. אנא הכנס מספר פלאפון תקין."))
            continue
        # If the phone number is valid, format it (to israeli format) and return it
        phone_number = "+972" + phone_number[1:]
        return phone_number


# Function to get user's prayer version (Nosach)
def get_Nosach():
    while True:
        Nosach = input(get_display("מה נוסח התפילה שלך?"))

        if Nosach not in ["אשכנז", "ספרד", "עדות המזרח", "Ashkenaz", "Sfard", "Edot Hamizrach", ""]:
            print(get_display("הנוסח שהכנסת אינו תקין. אנא הכנס נוסח תקין."))
            continue

        if Nosach == "":
            Nosach = "Sfard"
        if Nosach == "אשכנז":
            Nosach = "Ashkenaz"
        if Nosach == "ספרד":
            Nosach = "Sfard"
        if Nosach == "עדות המזרח":
            Nosach = "Edot Hamizrach"
        return Nosach

# Function to get user's location
def get_location():
    while True:
        location = input(get_display("מה מקום מגוריך?"))

        if location not in ["ירושלים", "תל אביב", "חיפה", "באר שבע", "Jerusalem", "Tel Aviv", "Haifa", "Beer Sheva", ""]:
            print(get_display("המקום שהכנסת אינו תקין. אנא הכנס מקום תקין."))
            continue

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

# Main function
def main():
    # Get user information
    user_phone_number = get_phone_number()
    user_Nosach = get_Nosach()
    user_location = get_location()
    
    # Get current day of the Omer
    today = what_day_is_it(user_location)
    
    # Build message for the user
    message = build_message_for_user(today, user_Nosach)
    
    # Send WhatsApp reminders until the end of the Omer period
    while today <= 49:
        today = what_day_is_it(user_location)
        message = build_message_for_user(today, user_Nosach)
        send_Whatsapp_messege(get_display(message), user_phone_number)
        time.sleep(24*60*60)  # Wait for a day
    print(get_display("סיימתי לשלוח תזכורות!"))
    return
    
if __name__ == "__main__":
    main()
