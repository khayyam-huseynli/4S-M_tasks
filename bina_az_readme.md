# Bina.az Mənzil Məlumatları Scraper

Bu layihə, Bina.az saytından satılıq mənzillərin məlumatlarını avtomatik olaraq toplayır və CSV faylına ixrac edir. Selenium və Python istifadə edərək, mənzillərin qiyməti, məkanı, otaq sayı, sahəsi və digər məlumatlarını çəkmək üçün nəzərdə tutulmuşdur.

## Xüsusiyyətlər

- Bina.az saytından satılıq mənzillərin avtomatik olaraq məlumatlarını toplamaq
- Çoxsəhifəli scraping imkanı
- Toplanan məlumatlar:
  - Qiymət
  - Məkan (rayon/şəhər)
  - Otaq sayı
  - Sahə (m²)
  - Mərtəbə
  - Elanın tarixi
  - Elanın linki
  - Şəkil URL-i
- Nəticələrin CSV faylına ixracı
- Avtomatik statistik analiz:
  - Orta/minimum/maksimum qiymət
  - Ən çox elan olan rayonlar
  - Otaq sayına görə paylanma

## Tələblər

- Python 3.7 və ya daha yuxarı
- Chrome brauzeri
- ChromeDriver (webdriver-manager paketindən avtomatik quraşdırılır)
- İnternet bağlantısı

## Quraşdırma

### 1. Virtual mühitin yaradılması və aktivləşdirilməsi

```bash
# Virtual mühit yaradılması
python -m venv 4sim_env

# Windows üçün aktivləşdirmə
4sim_env\Scripts\activate

# Linux/Mac üçün aktivləşdirmə
source 4sim_env/bin/activate
```

### 2. Tələb olunan paketlərin quraşdırılması

Layihədə tələb olunan paketləri requirements.txt faylından quraşdıra bilərsiniz:

```bash
pip install -r requirements.txt
```

Və ya əl ilə quraşdıra bilərsiniz:

```bash
pip install pandas selenium webdriver-manager
```

### 3. Chrome brauzerin quraşdırılması

Skript Chrome brauzeri istifadə edir. Əgər kompüterinizdə Chrome quraşdırılmayıbsa, [buradan](https://www.google.com/chrome/) endirə bilərsiniz.

## İstifadə qaydası

### 1. Skriptin işlədilməsi

```bash
python bina_az_scraper.py
```

### 2. Parametrlərin tənzimlənməsi

Skriptdə `scrape_bina_az` funksiyasını çağırarkən səhifə sayını dəyişə bilərsiniz:

```python
# Məsələn, 5 səhifədən məlumat çəkmək üçün:
properties_df = scrape_bina_az(5)
```

### 3. Nəticələrə baxış

Skript işləməyə başladıqdan sonra konsola aşağıdakı məlumatlar çıxarılacaq:
- Hər səhifədə tapılan elanların sayı
- Gözləmə vaxtı (sayta çox yük vurmamaq üçün)
- Əldə edilmiş məlumatların qısa xülasəsi
- Qiymət statistikası və məkan statistikası

Nəticələr `bina_az_properties.csv` faylına saxlanılacaq.

## Kod strukturu

- `setup_driver()`: Chrome webdriver-i konfiqurasiya edir
- `scrape_bina_az(num_pages)`: Təyin edilmiş sayda səhifədən məlumatları çəkir
- Əsas proqram:
  - Məlumatları çəkir
  - CSV faylına saxlayır
  - Sadə statistika göstərir

## Özəlləşdirmə imkanları

1. **Fərqli sayt parametrləri**: 
   ```python
   url = f"https://bina.az/alqi-satqi?page={page}"
   ```
   linkini dəyişərək kirayə evlər və ya digər kateqoriyalara uyğunlaşdıra bilərsiniz.

2. **Headless rejimini söndürmək**: 
   ```python
   chrome_options.add_argument('--headless')
   ```
   sətirini şərh kimi qeyd etməklə, brauzerin görünməsini təmin edə bilərsiniz.

3. **Gözləmə vaxtlarını dəyişmək**:
   ```python
   delay = random.uniform(1.0, 3.0)
   ```
   sətrindəki dəyərləri dəyişərək gözləmə vaxtını tənzimləyə bilərsiniz.

## Vacib qeydlər

1. **Etik scraping**: Sayta həddindən artıq yük vurmayın, gözləmə vaxtlarını azaltmayın.
2. **User-Agent**: Ehtiyac olduqda, `chrome_options.add_argument('--user-agent=...')` əlavə edərək istifadəçi agentini dəyişə bilərsiniz.
3. **IP məhdudiyyətləri**: Çox sayda sorğu göndərdikdə, sayt IP ünvanınızı bloklaya bilər. Proxy istifadə etmək lazım ola bilər.
4. **HTML strukturu dəyişiklikləri**: Bina.az saytının strukturu dəyişərsə, kod işləməyə bilər və yenilənməlidir.

## Xətalar və həllər

### Problem: `WebDriverException: Chrome failed to start`

Həll: Chrome brauzerin son versiyasını quraşdırın və ya ChromeDriver versiyasını brauzerinizin versiyasına uyğun olaraq dəyişin.

### Problem: `No such element exception`

Həll: HTML elementləri tapıla bilmir. Saytın strukturu dəyişmiş ola bilər. Selector-ları yoxlayın və yeniləyin.

## Lisenziya

Bu layihə MIT lisenziyası altında yayımlanmışdır. Daha ətraflı məlumat üçün LICENSE faylına baxın.

## Təşəkkürlər

- Selenium - veb-avtomatlaşdırma kitabxanası
- Pandas - məlumat təhlili üçün kitabxana
- Webdriver-manager - webdriver-in avtomatik idarə edilməsi

---

**Qeyd**: Bu skript yalnız tədqiqat və təhsil məqsədləri üçün istifadə edilməlidir. Bina.az və digər saytlardan məlumat çəkərkən, saytın istifadə şərtlərini və müvafiq qanunvericiliyi nəzərə alın.
