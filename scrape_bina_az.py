import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Selenium quraşdırılması
def setup_driver():    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Brauzeri görünmədən işlətmək üçün
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Webdriver quraşdırılması
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_bina_az(num_pages=3):
    """
    Bina.az saytından satılıq mənzillərin məlumatlarını çəkmək üçün funksiya
    """
    driver = setup_driver()
    
    # Nəticələri saxlamaq üçün list
    all_properties = []
    
    try:
        # Təyin edilmiş sayda səhifə üçün dövrə
        for page in range(1, num_pages + 1):
            # Satılıq mənzillər səhifəsi
            url = f"https://bina.az/alqi-satqi?page={page}"
            driver.get(url)
            
            # Səhifənin tam yüklənməsini gözləyək
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "items-i"))
            )
            
            # Elanların siyahısı
            property_items = driver.find_elements(By.CLASS_NAME, "items-i")
            
            print(f"Səhifə {page}: {len(property_items)} elan tapıldı")
            
            # Hər bir elan üçün məlumatları çəkək
            for item in property_items:
                try:
                    # Əsas məlumatlar
                    price = item.find_element(By.CLASS_NAME, "price").text.strip()
                    location = item.find_element(By.CLASS_NAME, "location").text.strip()
                    
                    # Parametrlər (otaq sayı, sahə və mərtəbə)
                    room_count = "N/A"
                    area = "N/A"
                    floor = "N/A"

                    params = item.find_elements(By.CLASS_NAME, "name")
                    parameters = params[0].text.strip().split('\n')

                    if len(parameters) == 1:
                        area = parameters[0]
                    elif len(parameters) > 1:
                        area = parameters[1]

                    room_count = parameters[0].split(' ')[0].strip() if (len(parameters) > 1 and parameters[0].split(' ')[1] == 'otaqlı') else "N/A"                    
                    floor = parameters[2].split(' ')[0].strip() if len(parameters) > 2 else "N/A"
                    
                    # Elanın tarixini alaq
                    try:
                        date = item.find_element(By.CLASS_NAME, "city_when").text.strip().split(',')[1].strip()
                    except:
                        date = "N/A"
                    
                    # Elanın URL-i
                    try:
                        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    except:
                        link = "N/A"
                    
                    # Elanın şəklini alaq
                    try:
                        image = item.find_element(By.TAG_NAME, "img").get_attribute("data-src")
                    except:
                        image = "N/A"
                    
                    # Məlumatları lüğət şəklində saxlayaq
                    property_data = {
                        "Qiymət": price,
                        "Məkan": location,
                        "Otaq sayı": room_count,
                        "Sahə": area,
                        "Mərtəbə": floor,
                        "Tarix": date,
                        "Link": link,
                        "Şəkil": image
                    }
                    
                    all_properties.append(property_data)
                
                except Exception as e:
                    print(f"Elan məlumatlarını çəkərkən xəta: {e}")
            
            # Sayta gələn yükü azaltmaq üçün qısa fasilə verək
            delay = random.uniform(1.0, 3.0)
            print(f"{delay:.2f} saniyə gözlənilir...")
            time.sleep(delay)
    
    except Exception as e:
        print(f"Scraping zamanı xəta baş verdi: {e}")
    
    finally:
        # Brauzeri bağlayaq
        driver.quit()
    
    # Nəticələri DataFrame-ə çevirək
    df = pd.DataFrame(all_properties)
    
    return df

# Əsas proqram
if __name__ == "__main__":
    print("Bina.az saytından məlumatlar çəkilir...")
    
    # 3 səhifədən məlumat çəkək
    properties_df = scrape_bina_az(3)
    
    # Nəticələri göstərək
    print("\nƏldə edilmiş məlumatlar:")
    print(f"Cəmi {len(properties_df)} elan məlumatı çəkildi")
    print(properties_df.head())
    
    # Məlumatları CSV faylına saxlayaq
    properties_df.to_csv("bina_az_properties.csv", index=False, encoding="utf-8-sig")
    print("\nMəlumatlar 'bina_az_properties.csv' faylına saxlanıldı")
    
    # Qısa statistika göstərək
    if not properties_df.empty:
        # Qiymət statistikası (təmizləmək lazımdır)
        # Qiymətləri ədədə çevirək (AZN və digər simvolları təmizləyək)
        try:
            # Qiymətləri təmizləyək və AZN-i silib ədədə çevirək
            properties_df['Təmiz qiymət'] = properties_df['Qiymət'].str.replace('AZN', '').str.replace(' ', '').astype(float)
            
            print("\nQiymət statistikası:")
            print(f"Orta qiymət: {properties_df['Təmiz qiymət'].mean():.2f} AZN")
            print(f"Minimum qiymət: {properties_df['Təmiz qiymət'].min():.2f} AZN")
            print(f"Maksimum qiymət: {properties_df['Təmiz qiymət'].max():.2f} AZN")
        except:
            print("Qiymət statistikasını hesablamaq mümkün olmadı")
        
        # Məkan statistikası - ən çox elan olan rayonlar
        print("\nƏn çox elan olan rayonlar:")
        print(properties_df['Məkan'].value_counts().head())
        
        # Otaq sayına görə statistika
        print("\nOtaq sayına görə paylanma:")
        print(properties_df['Otaq sayı'].value_counts())