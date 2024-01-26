import requests
from bs4 import BeautifulSoup

def get_last_email_opened_days_ago(user_id): #accesses specific customer from website
    url = f'https://docs.google.com/spreadsheets/d/1TWCwKJzZtIe4zoxuxrZpfw2MexZ2Rxc-qjA7f_DUn9Q/edit?usp=sharing/{user_id}/email_activity'
    
    try: #request to access
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser') #parses
    
    last_email_opened_days_ago = int(soup.find('span', class_='last email opened').text) #finds info
    return last_email_opened_days_ago

def calculate_personalized_discount(user_id):
    last_email_opened_days_ago = get_last_email_opened_days_ago(user_id)
    
    if last_email_opened_days_ago is not None:
        if last_email_opened_days_ago <= 7:  # active users
            discount_percentage = 10
        elif last_email_opened_days_ago <= 30:  # semi-active users
            discount_percentage = 5
        else:  # inactive users
            discount_percentage = 2
        return discount_percentage
    else: #if retrieval fails
        return None

def generate_discount_email(user_name, discount_percentage):
    if discount_percentage == 10:
        message = f"Hi {user_name},\n\nCongratulations! As an active user, you've earned a 10% discount on your favorite snacks. Use code ACTIVE10 at checkout. Happy snacking!"
    elif discount_percentage == 5:
        message = f"Hi {user_name},\n\nGreat news! You're a valued customer, and we're offering you a 15% discount on your next snack purchase. Use code VALUED15 at checkout. Enjoy!"
    elif discount_percentage == 2:
        message = f"Hi {user_name},\n\nWe miss you! As a special offer, here's a 20% discount to welcome you back. Use code WELCOME20 at checkout. We hope you find something you love!"
    else:
        message = ""
    return message
