from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

app = Flask(__name__, template_folder='templates', static_folder='static')

# ตัวแปรเก็บราคาล่าสุด
current_price = "กำลังโหลด..."

def fetch_price():
    global current_price

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ทำงานแบบไม่แสดง UI
    driver = webdriver.Chrome(options=options)

    while True:
        try:
            driver.get('https://www.simummuangmarket.com/en/product/287') 
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                '//*[@id="frontend_app"]/div[2]/main/div/div/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/strong'))
            )

            price_text = price_element.text.strip()

            if price_text and "บาท" in price_text:
                clean_price = ""
                for char in price_text:
                    if char.isdigit() or char == '.':
                        clean_price += char
                    else:
                        break
                current_price = f"{clean_price} บาท/กก."
            else:
                current_price = "ไม่พบข้อมูล"

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
            current_price = "ไม่พบข้อมูล"

        time.sleep(5)  # อัปเดตทุก 5 วินาที


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get-price')
def get_price():
    return current_price


if __name__ == '__main__':
    # เริ่ม thread สำหรับดึงราคา
    thread = threading.Thread(target=fetch_price)
    thread.daemon = True
    thread.start()

    # เริ่ม Flask Server
    app.run(debug=True)