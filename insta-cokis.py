from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os
import requests  # لإرسال الملف إلى تيليجرام


# =============================================
# شعار Gordon باللون الأحمر الغامق
# =============================================
def print_gordon_logo():
    RED_BOLD = "\033[1;31m"
    RESET = "\033[0m"
    logo = f"""
{RED_BOLD}
 ██████╗  ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗
██╔════╝ ██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║
██║  ███╗██║   ██║██████╔╝██║  ██║██║   ██║██╔██╗ ██║
██║   ██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╗██║
╚██████╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝██║ ╚████║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝

██╗███╗   ██╗███████╗████████╗ █████╗  
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗
██║██╔██╗ ██║███████╗   ██║   ███████║
██║██║╚██╗██║╚════██║   ██║   ██╔══██║
██║██║ ╚████║███████║   ██║   ██║  ██║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

██╗██╗  ██╗ █████╗ ██████╗  ██████╗ 
██║██║  ██║██╔══██╗██╔══██╗██╔═══██╗
██║███████║███████║██████╔╝██║   ██║
██║██╔══██║██╔══██║██╔══██╗██║   ██║
██║██║  ██║██║  ██║██████╔╝╚██████╔╝
╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ 

  v2.0 - Instagram Cookie Extractor (Gordon) telrgram:@qe4_7
{RESET}
"""
    print(logo)


def send_file_to_telegram(file_path, bot_token, chat_id):
    """
    إرسال ملف إلى تيليجرام باستخدام البوت.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': chat_id}
        try:
            response = requests.post(url, files=files, data=data, timeout=30)
            if response.status_code == 200:
                print("\033[1;32m✅ تم إرسال الملف إلى تيليجرام بنجاح!\033[0m")
                return True
            else:
                print(f"\033[1;31m❌ فشل الإرسال: {response.text}\033[0m")
                return False
        except Exception as e:
            print(f"\033[1;31m❌ خطأ أثناء الإرسال: {e}\033[0m")
            return False


def main():
    print_gordon_logo()
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;33m🍪 أداة استخراج الكوكيز من إنستغرام (يدوياً)\033[0m")
    print("\033[1;36m" + "=" * 60 + "\033[0m")

    # طلب اسم المستخدم
    username = input("\033[1;37m👤 أدخل اسم المستخدم (سيُستخدم في اسم ملف الكوكيز): \033[0m").strip()
    if not username:
        username = "unknown"
        print("\033[1;31m⚠️  لم تدخل اسماً، سيتم استخدام 'unknown'.\033[0m")

    # تحديد مسار الملف
    filename = f"cookies_{username}.json"
    filepath = filename  # في المجلد الحالي

    print(f"\n\033[1;32m📁 سيتم حفظ الكوكيز في: {filepath}\033[0m")

    print("\n\033[1;34m🚀 سيفتح المتصفح الآن. سجل دخولك إلى Instagram يدوياً.\033[0m")
    input("\033[1;33m⏳ بعد فتح المتصفح وتسجيل الدخول، اضغط Enter هنا...\033[0m")

    # إعداد المتصفح بدون أي خيارات إخفاء (طبيعي)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.instagram.com/")

    # ننتظر حتى يسجل المستخدم دخوله يدوياً
    input("\033[1;33m✅ إذا كنت قد سجلت الدخول بالفعل، اضغط Enter لحفظ الكوكيز...\033[0m")

    cookies = driver.get_cookies()
    cookie_dict = {c['name']: c['value'] for c in cookies}

    # حفظ الملف
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cookie_dict, f, indent=2, ensure_ascii=False)

    print(f"\n\033[1;32m✅ تم حفظ الكوكيز بنجاح في: {filepath}\033[0m")
    print(f"\033[1;32m📦 عدد الكوكيز: {len(cookies)}\033[0m")

    driver.quit()

    # ===== خيار الإرسال إلى تيليجرام =====
    send_choice = input("\n\033[1;33m📤 هل تريد إرسال ملف الكوكيز إلى تيليجرام؟ (y/n): \033[0m").strip().lower()
    if send_choice in ['y', 'yes', 'نعم', 'Y']:
        bot_token = input("\033[1;37m🤖 أدخل توكن البوت (Bot Token): \033[0m").strip()
        chat_id = input("\033[1;37m🆔 أدخل معرف الشات (Chat ID): \033[0m").strip()
        if bot_token and chat_id:
            print("\n\033[1;34m⏳ جاري إرسال الملف...\033[0m")
            send_file_to_telegram(filepath, bot_token, chat_id)
        else:
            print("\033[1;31m⚠️  لم تدخل التوكن أو المعرف، تم تخطي الإرسال.\033[0m")

    print("\n\033[1;35m🔚 انتهى البرنامج. شكراً لاستخدامك أداة Gordon!\033[0m")


if __name__ == "__main__":
    main()