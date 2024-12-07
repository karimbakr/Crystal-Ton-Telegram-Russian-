import httpx
import json
import random
import asyncio
from time import sleep
from datetime import datetime
from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import Spinner
import pyfiglet
import os
import subprocess
import sys
import importlib.util
libraries = ["requests", "colorama", "rich"," pyfiglet","httpx","asyncio"]

def is_library_installed(library_name):
    """تحقق إذا كانت المكتبة مثبتة."""
    return importlib.util.find_spec(library_name) is not None

def install_libraries():
    for library in libraries:
        if is_library_installed(library):
            print(f"✅ {library} is already installed.")
        else:
            try:
                print(f"🔄 Installing {library}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                print(f"✅ {library} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {library}. Error: {e}")
install_libraries()                
console = Console()
def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text,font='slant').splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)  # Green
        elif i < section_size * 2:
            print(colors[1] + line)  # Yellow
        else:
            print(colors[2] + line)  # Red

def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]  # Cycle through colors
        print(color + f'| {social}: {username} |')
    
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
  
def get_user_agent():
    return "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 Telegram-Android/11.2.2 (Xiaomi M1908C3JGG; Android 12; SDK 31; AVERAGE)"

def wait_with_random_delay(message: str = "Processing your request..."):
    """
    دالة انتظار احترافية بوقت عشوائي بين 40 و60 ثانية.
    
    Args:
    message (str): الرسالة التي تظهر أثناء الانتظار.
    """
    # اختيار وقت عشوائي بين 40 و60 ثانية
    delay = random.randint(5, 10)
    
    with console.status(f"[bold cyan]{message}", spinner="dots") as status:
        for i in range(delay):
            sleep(1)  # انتظار لمدة ثانية واحدة
            status.update(f"[bold green]{message} ({i+1}/{delay} seconds)")
    
    console.print(f"[bold magenta]Done! Total wait time: {delay} seconds.[/bold magenta]")
# تهيئة مكتبة colorama
init(autoreset=True)

# اسم الملف الخارجي الذي يحتوي على initDataStr
data_file = "data.txt"

# دالة لإضافة التاريخ والوقت للطباعة
def log_message(message, color=Fore.WHITE):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {message}{Style.RESET_ALL}")

# دالة لجلب initDataStr من الملف الخارجي
def get_init_data():
    try:
        with open(data_file, "r") as file:
            init_data = file.read().strip()
            log_message(f"Loaded initDataStr from {data_file}.", Fore.GREEN)
            return init_data
    except FileNotFoundError:
        log_message(f"Error: File '{data_file}' not found.", Fore.RED)
        return None

# دالة لإرسال الطلب
def send_request():
    # جلب initDataStr من الملف الخارجي
    init_data_str = get_init_data()
    if not init_data_str:
        log_message("initDataStr is missing. Aborting request.", Fore.RED)
        return None, None  # إرجاع None في حالة الفشل

    url = "https://test.diamondsday.ru/api/register"

    payload = {
        "initDataStr": init_data_str,
        "version": "7.10",
        "platform": "ios"
    }

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': "Bearer null",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': '"Android"',
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/"
    }

    try:
        log_message("Sending request to the server...", Fore.BLUE)
        # إرسال الطلب
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)

        # التحقق من حالة الرد
        if response.status_code == 200:
            response_data = response.json()

            # استخراج token و first_name
            token = response_data.get("token", "Token not found")
            first_name = response_data.get("user", {}).get("first_name", "First name not found")
            
            log_message(f"Request successful. Token: {token}", Fore.GREEN)
            log_message(f"User First Name: {first_name}", Fore.CYAN)
            
            return token, first_name  # إرجاع القيم بشكل صحيح
        else:
            log_message(f"Request failed with status code: {response.status_code}", Fore.RED)
            log_message(f"Response: {response.text}", Fore.YELLOW)
            return None, None

    except Exception as e:
        log_message(f"An error occurred: {e}", Fore.RED)
        return None, None

# دالة لإرسال طلب النقر
def send_click_request(token):
    url = "https://test.diamondsday.ru/api/clicks"
    total = int("1")
    payload = {
        "clicks": total
    }

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/clicker",
        
    }

    try:
        log_message("Sending POST request...", Fore.BLUE)
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            # استخراج البيانات من الاستجابة
            response_data = response.json()
            

            # استخراج القيم المطلوبة من داخل "user"
            user_data = response_data.get("user", {})
            energy = user_data.get("energy", "Energy not found")
            level = user_data.get("level", "Level not found")
            total_clicks = user_data.get("total_clicks", "Total clicks not found")
            tone = user_data.get("ton_balance", "ton_balance not found")

            # طباعة القيم المستخرجة
            log_message(f"Your Energy: [{energy}]", Fore.GREEN)
            log_message(f"Your Level: [{level}]", Fore.CYAN)
            log_message(f"Your Blance: [{total_clicks}]", Fore.YELLOW)
            log_message(f"Your Ton: [{tone}]", Fore.YELLOW)
            log_message(Fore.GREEN+"You win: " + Fore.YELLOW + f"[{total}]" + " crystal" )
            if energy <= 50:
            	log_message(f"Your Energy down 50: [{energy}] Script Well working After Charging..", Fore.RED)
            	import time
            	time.sleep(1800)
            if tone >= 2:
            	log_message(f"Your Ton is : [{tone}] You Can Withdrawal Now ", Fore.YELLOW)
            	
            	

        else:
            log_message(f"Request failed with status code {response.status_code}: {response.text}", Fore.RED)
    except httpx.RequestError as e:
        log_message(f"An error occurred: {e}", Fore.RED)





# دالة لإرسال الطلب
async def send_daily_ton_request(token):
    url = "https://test.diamondsday.ru/api/awards/daily_ton"

    payload = {}

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/boost",
        
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 500 or response.status_code ==200 :
            # استخراج message من الرد
            response_json = response.json()
            #print(response_json)  # تحويل النص إلى JSON
            message = response_json.get('message', 'Message not found')
            log_message(Fore.GREEN+"daily Ton : "+Fore.RED+f" {message}" )

    # طباعة الاستجابة
   

# تشغيل الدالة





async def spin_fortune_wheel(token):
    url = "https://test.diamondsday.ru/api/fortune_wheel/spin"
    
    payload = {}
    
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/fortune",
        
    }
    
    async with httpx.AsyncClient() as client:
        for i in range(3):  # إرسال الطلب 3 مرات
            #print(f"Sending request {i + 1}...")
            response = await client.post(url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                
                # استخراج الـ JSON من الرد
                response_data = response.json()
                
                clicks = response_data.get('clicks')
                tries_left = response_data.get('tries_left')
                
                log_message(f"Your Win spin: [{clicks}]", Fore.GREEN)
                log_message(f"Your  spin left: [{tries_left}]", Fore.GREEN)
            elif response.status_code == 500:
                log_message("You already finished spin today", Fore.GREEN)
                break
                
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)
            
            # الانتظار لمدة 5 ثوانٍ بين كل إرسال لتجنب الحظر
            await asyncio.sleep(5)



# القائمة التي تحتوي على القيم المطلوبة


# دالة لإرسال الطلبات لكل قيمة في القائمة
async def complete_award(token):
    types_list = [
    "telegram_ru",
    "superclick",
    "youtube",
    "fortune_visit",
    "link_share"
]
    url = "https://test.diamondsday.ru/api/awards/complete"
    
    # تكرار القيم في القائمة
    for type_value in types_list:
        payload = {
            "type": type_value
        }

        headers = {
            'User-Agent': get_user_agent(),
            'Accept': "application/json",
            'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            'Accept-Language': "en",
            'sec-ch-ua-mobile': "?1",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/json;charset=utf-8",
            'sec-ch-ua-platform': "\"Android\"",
            'Origin': "https://test.diamondsday.ru",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://test.diamondsday.ru/boost",
            
        }

        # إرسال الطلب لكل نوع في القائمة
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response_json = response.json()  # تحويل النص إلى JSON
            message = response_json.get('message', 'Message not found')
            log_message(Fore.GREEN+"Task : "+Fore.RED+f"{message} " +f"Task Name : {type_value}")

        # طباعة الرد للاستجابة
        #print(f"Response for type '{type_value}': {response.text}")
        
        # تأخير بين كل طلب وآخر لتجنب الحظر
        await asyncio.sleep(10)  # تأخير لمدة 2 ثانية (يمكنك تعديل المدة حسب الحاجة)

# استدعاء الدالة


async def send_requestadd(token):
    url = "https://test.diamondsday.ru/api/ads"

    # إنشاء عميل HTTPX
    async with httpx.AsyncClient() as client:
        # تكرار الإرسال ثلاث مرات
        for i in range(1, 4):
            payload = {
                "ads_id": i  # تغيير قيمة ads_id في كل مرة
            }

            headers = {
                'User-Agent': get_user_agent(),
                'Accept': "application/json",
                'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
                'Accept-Language': "en",
                'sec-ch-ua-mobile': "?1",
                'Authorization': f"Bearer {token}",
                'Content-Type': "application/json;charset=utf-8",
                'sec-ch-ua-platform': "\"Android\"",
                'Origin': "https://test.diamondsday.ru",
                'Sec-Fetch-Site': "same-origin",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Referer': "https://test.diamondsday.ru/ads",
            }

            try:
                # إرسال الطلب باستخدام httpx
                response = await client.post(url, data=json.dumps(payload), headers=headers)
                
                # تحويل النص إلى JSON
                try:
                    response_json = response.json()
                except json.JSONDecodeError:
                    log_message(Fore.RED + "Failed to decode JSON response")
                    continue
                
                # التحقق من نوع الاستجابة
                if isinstance(response_json, dict):
                    message = response_json.get('message', 'Done ')
                elif isinstance(response_json, list) and len(response_json) > 0:
                    message = response_json[0].get('message', 'Done') if isinstance(response_json[0], dict) else 'Invalid format'
                else:
                    message = 'Invalid response format'

                # طباعة الرسالة
                log_message(Fore.GREEN + "add watching: " + Fore.RED + f"{message}")
            except httpx.RequestError as e:
                log_message(Fore.RED + f"Request error: {e}")
            except Exception as e:
                log_message(Fore.RED + f"Unexpected error: {e}")

            # تأخير 30 ثانية بين كل طلب
            await asyncio.sleep(10)

        # بعد إتمام الإعلانات، الانتظار 4 ساعات
        log_message("Waiting for 4 hours before sending the next advertisement...", Fore.YELLOW)
        

# استدعاء الدالة باستخدام asyncio
async def main():
    
    await send_requestadd(token)

# تشغيل البرنامج
    

# دالة لإرسال الطلب باستخدام httpx
def send_award_request(token):
    url = "https://test.diamondsday.ru/api/awards/daily"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/boost",
        
    }
    payload = {}

    try:
        # استخدام مكتبة httpx لإرسال الطلب
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)

        # التحقق من حالة الاستجابة
        if response.status_code == 500 or response.status_code ==200 :
            # استخراج message من الرد
            response_json = response.json()
            #print(response_json)  # تحويل النص إلى JSON
            message = response_json.get('message', 'Done ')
            log_message(Fore.GREEN+"daily login : "+Fore.RED+f" {message}" )  # استخراج message
            
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        print(f"An error occurred: {e}")

# استدعاء الدالة


# دالة لإرسال الطلب إلى API


# دالة لإرسال الطلب إلى API
async def send_card_request(token):
    url = "https://test.diamondsday.ru/api/cards"

    payload = {
        "card_id": 1
    }

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://test.diamondsday.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://test.diamondsday.ru/cards",
        
    }

    async with httpx.AsyncClient() as client:
        # إرسال الطلب
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 500 or response.status_code ==200 :
            # استخراج message من الرد
            response_json = response.json()
            #print(response_json)  # تحويل النص إلى JSON
            message = response_json.get('message', 'Done')
            log_message(Fore.GREEN+"Card Up : "+Fore.RED+f" {message}" )

    # طباعة الاستجابة
    #print(response.text)

# استدعاء الدالة

token, first_name = send_request()

if token:
    
    banner_text = "Crystal Ton"
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner(banner_text)
    social_media_usernames = [
        ("Telegram Channel", "https://t.me/YOU742"),
        
        #("", "@"),
        ("Coder", "@Ke4oo"),
        ("Coder", "Karim"),
    ]
    
    print_info_box(social_media_usernames)
    log_message(f"Welcome {first_name}!", Fore.GREEN)
    userask = input(str(Fore.BLUE +"Do You wont Up Card ?  [y or n] : "))
    
    asyncio.run(main())
    asyncio.run(complete_award(token))
    send_award_request(token)
    asyncio.run(send_daily_ton_request(token)) 
    asyncio.run(spin_fortune_wheel(token))
    if userask == "y" or userask =="Y":
    	asyncio.run(send_card_request(token))    
    while True:
    	send_click_request(token)
    	wait_with_random_delay("Waiting to send next job...")
    
else:
    log_message("No token received. Cannot proceed.", Fore.RED)
