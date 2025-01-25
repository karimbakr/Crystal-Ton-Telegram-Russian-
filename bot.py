import aiohttp
import asyncio
import json
from colorama import Fore, init, Style
from datetime import datetime
import pyfiglet
import os
import importlib.util 
import  subprocess
import sys

import random
# تهيئة مكتبة colorama
libraries = ["aiohttp","colorama",  "pyfiglet","asyncio"]

# تهيئة colorama لدعم الألوان في الأنظمة المختلفة
init(autoreset=True)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_library_installed(library_name):
    """تحقق إذا كانت المكتبة مثبتة."""
    return importlib.util.find_spec(library_name) is not None

def install_libraries():
    for library in libraries:
        if is_library_installed(library):
            print(f"✅ {library} is already installed.")
            clear_screen()
        else:
            try:
                print(f"🔄 Installing {library}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                print(f"✅ {library} installed successfully!")
                clear_screen()
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {library}. Error: {e}")

install_libraries()
init(autoreset=True)

# دالة لقراءة قيمة initDataStr من ملف خارجي
def get_init_data_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            init_data = file.read().strip()
            return init_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# دالة للحصول على التاريخ والوقت الحالي بتنسيق معين
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# دالة لإرسال طلب تسجيل والحصول على التوكين

def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text, font='slant').splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)
        elif i < section_size * 2:
            print(colors[1] + line)
        else:
            print(colors[2] + line)

# دالة لطباعة معلومات حول القنوات الاجتماعية
def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]
        print(color + f'| {social}: {username} |')
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
async def send_request():
    url = "https://crystalton.ru/api/user"
    
    # قراءة initDataStr من الملف
    init_data_str = get_init_data_from_file("data.txt")
    if not init_data_str:
        print(f"{Fore.RED}[{get_current_datetime()}] Your Token is wrong put your token not queryid !")
        return None
    
    # إعداد البيانات
    
    # إعداد الرؤوس
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {init_data_str}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                # استخراج التوكين
                token = init_data_str
                first_name = data.get("user", {}).get("first_name", "Unknown")
                print(f"{Fore.GREEN}[{get_current_datetime()}] Token: {token}")
                print(f"{Fore.GREEN}[{get_current_datetime()}] First Name: {first_name}")
                return token
            else:
                print(f"{Fore.RED}[{get_current_datetime()}] Error: {response.status} - {await response.text()}")
                return None

# دالة لإرسال الطلبات للإعلانات باستخدام التوكين
async def send_ads_requests(token):
    url = "https://crystalton.ru/api/ads/view"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/ads",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
    }

    while True:  # تنفيذ الدالة بشكل متكرر
        for ads_id in range(1, 10):  # إرسال 3 طلبات بقيم ads_id مختلفة
            payload = {"ads_id": ads_id}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 500:
                        try:
                            error_data = await response.json()
                            error_message = error_data.get("message", "Done ad.")
                            print(f"{Fore.YELLOW}[{get_current_datetime()}] Ad Watching {ads_id}: {error_message}")
                    
                        except Exception:
                            error_message = await response.text()
                            
                    elif response.status == 200:
                        print(f"{Fore.YELLOW}[{get_current_datetime()}] Ad Watching {ads_id}: Done Ad")                                     
                    else:
                        print(f"{Fore.RED}[{get_current_datetime()}] Request {ads_id} Error: {response.status} - {await response.text()}")

            await asyncio.sleep(5)  # انتظار بسيط بين الطلبات

        print(f"{Fore.GREEN}[{get_current_datetime()}] Waiting for 4 hours before repeating Ad...")
        await asyncio.sleep(4 * 60 * 60)  # الانتظار لمدة 4 ساعات



async def send_spaceship(token):
    url = "https://crystalton.ru/api/spaceship"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/game"
    }

    async with aiohttp.ClientSession() as session:
        while True:  # يعمل بشكل مستمر كل ساعة
            for _ in range(5):  # إرسال الطلب 5 مرات
                random_score = random.randint(5000, 20000)  # توليد رقم عشوائي بين 5000 و20000
                payload = {"scores": random_score}
                
                
                async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                    if response.status == 200:                                      
                        print(f"{Fore.MAGENTA}[{get_current_datetime()}]Playing Space... Scores earned: {random_score}")                        
                    else:
                        print("Not ticket to play")
                
                await asyncio.sleep(60)  # الانتظار دقيقة بين كل طلب

            await asyncio.sleep(3600)
# استدعاء الدالة

def get_user_agent():
    return "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 Telegram-Android/11.2.2 (Xiaomi M1908C3JGG; Android 12; SDK 31; AVERAGE)"

# دالة لعمل Spin بشكل دوري كل 12 ساعة
async def spin_fortune_wheel(token):
    url = "https://crystalton.ru/api/fortune_wheel"
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
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/fortune",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
    }

    async with aiohttp.ClientSession() as session:
        while True:
	        for _ in range(3): 
	            async with session.post(url, data=json.dumps(payload), headers=headers) as response:
	                if response.status == 200 or response.status ==500:
	                    data = await response.json()
	                    error_message = data.get("message", "Done ad.")
	                    clicks = data.get('clicks', 'No data')
	                    tries_left = data.get('tries_left', 'No data')
	                    if error_message:
	                    	print(f"{Fore.YELLOW}[{get_current_datetime()}] spin: {error_message:}")
	                    else:
	                    	print(f"{Fore.YELLOW}[{get_current_datetime()}] Win spin: {clicks}")
	                    	print(f"{Fore.YELLOW}[{get_current_datetime()}] Left spin: {tries_left}")
	                    
	                else:
	                    print(f"Error: {response.status} - {await response.text()}")
	
	            # الانتظار لمدة 4 ثوانٍ بين كل طلب
	            await asyncio.sleep(4)
	        print(f"{Fore.GREEN}[{get_current_datetime()}] Waiting for 12 hours before repeating spin...")
	        await send_daily_award_request(token)
	        await send_ton(token)
	        await asyncio.sleep(43200)

# دالة غير متزامنة لإرسال الطلب
async def send_daily_award_request(token):
    url = "https://crystalton.ru/api/awards/daily"

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
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/boost",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload), headers=headers) as response:
            if response.status == 200 or response.status ==500:
	                    data = await response.json()
	                    error_message = data.get("message", "Done daily login.")
	                    
	                    if error_message:
	                    	print(f"{Fore.CYAN}[{get_current_datetime()}] daily login: {error_message:}")
	                    


# دالة غير متزامنة لإرسال طلب POST
async def send_ton(token):
    url = "https://crystalton.ru/api/awards/daily_ton"
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
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/boost",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
    }

    # إرسال الطلب باستخدام aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload), headers=headers) as response:
            # طباعة الاستجابة
            if response.status == 200 or response.status ==500:
	                    data = await response.json()
	                    error_message = data.get("message", "Done daily login ton.")
	                    
	                    if error_message:
	                    	print(f"{Fore.MAGENTA}[{get_current_datetime()}] daily login ton: {error_message:}")	                    
async def send_click_request(token):
    url = "https://crystalton.ru/api/clicks"
    payload = {"clicks": 1}

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'Accept-Language': "en",
        'sec-ch-ua-mobile': "?1",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json;charset=utf-8",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://crystalton.ru",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://crystalton.ru/clicker",
        'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
    }

    # إرسال الطلب غير المتزامن
    async with aiohttp.ClientSession() as session:
        while True:
	        async with session.post(url, json=payload, headers=headers) as response:
	            # التحقق من حالة الاستجابة
	            if response.status == 200:
	                # تحليل الاستجابة بتنسيق JSON
	                data = await response.json()
	                
	                # استخراج البيانات من المفتاح 'user'
	                user_data = data.get('user', {})
	                total_clicks = user_data.get('total_clicks', 'N/A')
	                country = user_data.get('country', 'N/A')
	                ton_balance = user_data.get('ton_balance', 'N/A')
	                energy = user_data.get('energy', 'N/A')
	
	                print(f"{Fore.BLUE}[{get_current_datetime()}] Total Clicks: [{total_clicks}]")
	                print(f"{Fore.CYAN}[{get_current_datetime()}] Country: [{country}]")
	                print(f"{Fore.CYAN}[{get_current_datetime()}] Ton: [{ton_balance}]")
	                print(f"{Fore.CYAN}[{get_current_datetime()}] energy: [{energy}]")
	                if energy <=50:
	                	print(f"{Fore.CYAN}[{get_current_datetime()}] energy is Down: [{energy}] script working after charging")
	                	await asyncio.sleep(1800)
	                	
	                await asyncio.sleep(5)
	                
	            else:
	                print(f"Error: Unable to fetch data, Status Code: {response.status}")	              
# تشغيل البرنامج



async def complete_award_from_file(token, file_path):
    # قراءة القيم من الملف
    with open(file_path, 'r') as file:        
            # إذا كان الملف بصيغة TXT
            lines = file.readlines()
            data = [line.strip() for line in lines]  # قراءة كل سطر وتخزينه كقيمة مستقلة

    url = "https://test.diamondsday.ru/api/awards/complete"
    
    # مؤشر للوصول للقيمة الحالية
    current_index = 0

    # إرسال الطلبات في حلقة لا نهائية
    while True:
        type_value = data[current_index]  # الحصول على القيمة الحالية من القائمة

        payload = {
            "type": f"{type_value}",
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
            'Cookie': "_ym_uid=1733992546227327601; _ym_d=1733992546; _ym_isad=2"
        }

        # إرسال الطلب
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response_json = await response.json()  # تحويل النص إلى JSON بشكل غير متزامن
                message = response_json.get('message', 'Message not found')
                print(f"[{type_value}] Task: {message}")

        # تأخير بين كل طلب وآخر لتجنب الحظر
        await asyncio.sleep(10)  # تأخير لمدة 10 ثواني (يمكنك تعديل المدة حسب الحاجة)

        # تحديث المؤشر للانتقال إلى القيمة التالية في الملف
        current_index += 1
        if current_index >= len(data):  # إذا وصلنا إلى نهاية القائمة، نعود إلى البداية
            break



async def main():
    create_gradient_banner("Crystal ton")  # عرض الشعار
    print_info_box([("Telegram", "https://t.me/YOU742"), ("Coder", "@Ke4oo")])  # معلومات وسائل التواصل
    print(Fore.GREEN + "Welcome to the Script!")
    token = await send_request()
    
    if token:
    	await asyncio.gather(
            send_ads_requests(token),
            spin_fortune_wheel(token),
            send_click_request(token),
            send_spaceship(token)
            
        ) 	    
# تشغيل البرنامج
asyncio.run(main())
