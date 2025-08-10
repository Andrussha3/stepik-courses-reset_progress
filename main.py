
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from data import curs_url,user_login,user_password # Берем наши переменные из файла data.py

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://stepik.org/catalog?auth=login')

# Ожидание и заполнение поля email


email_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "id_login_email"))
)
email_field.clear()
email_field.send_keys(user_login)

# Ожидание и заполнение поля пароля
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "id_login_password"))
)
password_field.clear()
password_field.send_keys(user_password)
# Клик по кнопке войти
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sign-form__btn.button_with-loader"))
)
button.click()
time.sleep(3)



driver.get(curs_url)# получаем URL нашего первого шага в курсе и выполняем переход на него



max_attempts = 9999  # Максимальное количество попыток
successful_resets = 0  # Счётчик успешных сбросов

for attempt in range(max_attempts):
    try:
        # Пытаемся найти и нажать кнопку "Решить снова"
        button_retry = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.again-btn.white"))
        )
        button_retry.click()
        successful_resets += 1
        print(f"Шаг {attempt + 1}: Кнопка 'Решить снова' нажата.")
    except TimeoutException:
        print(f"Шаг {attempt + 1}: Кнопка 'Решить снова' не найдена.")
    except ElementClickInterceptedException:
        print(f"Шаг {attempt + 1}: Кнопка 'Решить снова' перекрыта другим элементом.")
        continue  # Пропускаем итерацию, если кнопка не кликабельна

    try:
        # Пытаемся найти и нажать кнопку "Следующий шаг"
        button_next = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Следующий шаг']"))
        )
        button_next.click()
        print(f"Шаг {attempt + 1}: Кнопка 'Следующий шаг' нажата.")
    except TimeoutException:
        print(f"Шаг {attempt + 1}: Кнопка 'Следующий шаг' не найдена. Возможно, курс завершён.")
        break  # Выход из цикла, если кнопка "Следующий шаг" отсутствует
    except ElementClickInterceptedException:
        print(f"Шаг {attempt + 1}: Кнопка 'Следующий шаг' перекрыта другим элементом.")
        break  # Выход из цикла, если кнопка не кликабельна

# Завершение программы
print("\nПрограмма завершила свою работу.")
print(f"Всего шагов на курсе успешно сброшено: {successful_resets}")
driver.quit()  # Закрытие браузера
