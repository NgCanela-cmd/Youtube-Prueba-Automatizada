from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import os
import base64





def initialize_driver():
    service = Service(executable_path='F:\Zip + Java\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    return driver



def get_youtube_videos(driver):

    driver.get('https://www.youtube.com/')
    time.sleep(2)

    search_box = driver.find_element(By.NAME, 'search_query')
    search_box.send_keys('Hola soy german')
    serch_btn = driver.find_element(By.XPATH,'//*[@id="center"]/yt-searchbox/button')
    serch_btn.click()
    time.sleep(4)
    html = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de YouTube</title>
            <style>
                img {
                    width: 500px;
                    height: 500px;
                    align-items: center;
                }
                ul {
                    list-style-type: bullet;
                    text-align: center;
                    margin-left: 10px;
                    margin-right: 10px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    padding-left: 10px;
                    padding-right: 10px;
                    text-bold: true;
                }
                li {
                    margin-bottom: 10px;
                }
                h1 {
                    text-align: center;
                }
                h2 {
                    text-align: center;
                }
                body {
                    background-color: rgb(255, 255, 255);
                    content: "";
                    justify-content: center;
                    align-items: center;
                }   
                
            </style>
        </head>
        <body>
            <h1>Reporte de Prueba Automatizada</h1>

            <h2>Videos encontrados en YouTube con el título 'Hola soy german':</h2>
            <ul>
    """

    a = 0
    for s in range(6):
        a = a + 1
        path_german = os.path.join(os.path.expanduser("~"), "Imágenes", 'Videos_encontrados_{}.png').format(a)
        path_german1 = os.path.join(os.path.expanduser("~"), "Imágenes")
        driver.save_screenshot(path_german)
        driver.execute_script("window.scrollBy(0, 600)")

        with open(path_german, "rb") as img_file:
          img_german_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        html += f"<img src='data:image/png;base64,{img_german_base64}' width='500'/><br> <br>" 

        time.sleep(1) 
             
    print(f"Imagenes de los videos guardados en: {path_german1}")

    for _ in range(6):
        driver.execute_script("window.scrollBy(0, -600)")
        time.sleep(1)


    videos = driver.find_elements(By.ID, 'video-title')
    print("Nombres de los videos encontrados:\n")
    videos_encontrados = []
    for vds, video in enumerate(videos):
        titulo = video.get_attribute("title")
        if titulo:
            print(f"{vds+1}. {titulo}")
            videos_encontrados.append(titulo)


    os.makedirs(os.path.join(os.path.expanduser("~"), "Imágenes"), exist_ok=True)
    document = os.path.join(os.path.expanduser("~"), "Documents")
    R_html = os.path.join(document, "Reporte.html")

    

    for titulo in videos_encontrados:
        html += f"<li>{titulo}</li>"
       

    html += """
            </ul>
            
    """

    #filter_videos(driver)

    filter_btn = driver.find_element(By.XPATH,'//*[@id="filter-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
    filter_btn.click()
    time.sleep(2)
    path_filter = os.path.join(os.path.expanduser("~"), "Imágenes", "filter.png")
    path_filter1 = os.path.join(os.path.expanduser("~"), "Imágenes")
    driver.save_screenshot(path_filter)
    print(f"Captura de los filtros guardada en: {path_filter1}")
    filte_btn = driver.find_element(By.ID,'close-button')
    filte_btn.click()

    with open(path_filter, "rb") as img_file:
        img_filter_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    html += """
    <h2>Captura del Filtro:</h2>
    <img src="data:image/png;base64,""" + img_filter_base64 + """" width="1080"/>
    """
    with open(R_html, "w", encoding="utf-8") as archivo:
      archivo.write(html)
    time.sleep(1)

    try:
        tabs = driver.find_elements(By.XPATH, '//yt-chip-cloud-chip-renderer//a')
        for tab in tabs:
            if 'Canales' in tab.text:
                tab.click()
                break
        time.sleep(6)

        canal = driver.find_element(By.XPATH, '//a[@id="main-link"]')
        canal_encontrado = 'HolaSoyGerman' in canal.text
        if canal_encontrado:
            print("Canal 'Hola soy german' encontrado.")
            canal.click()
            time.sleep(4)

            path_german = os.path.join(os.path.expanduser("~"), "Imágenes", "canal_{}.png").format(canal_encontrado)
            path_german1 = os.path.join(os.path.expanduser("~"), "Imágenes")
            driver.save_screenshot(path_german)
            print(f"Captura del canal 'Hola soy german' guardada en: {path_german1}")

            with open(path_german, "rb") as img_file:
                img_german_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            html += """
            <h2>Captura del canal 'Hola soy german':</h2>
            <img src="data:image/png;base64,""" + img_german_base64 + """" width="1080"/>
            """
            time.sleep(1)
        else:
            html += "<p>Canal no coincide con el nombre.</p>"
    except NoSuchElementException:
        html += "<p>No se encontró canal con ese nombre.</p>"
        canal_encontrado = False

    with open(R_html, "w", encoding="utf-8") as archivo:
      archivo.write(html)


    list_video_btn = driver.find_element(By.XPATH,'//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[2]/div[1]')
    list_video_btn.click()
    time.sleep(2)
    for s in range(4):
         driver.execute_script("window.scrollBy(0, 700)")
         time.sleep(1)
 
    for s in range(4):
         driver.execute_script("window.scrollBy(0,-700)")
         
   
    list_video_btn = driver.find_element(By.XPATH,'//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[1]')
    list_video_btn.click()
    time.sleep(1)
 
    view_video = driver.find_element(By.XPATH, '//*[@id="items"]/ytd-grid-video-renderer[1]')
    view_video.click()
    time.sleep(20)  
 
    #skip_btn = driver.find_element(By.XPATH,'//*[@id="skip-button:2"]')
    #skip_btn.click()
 
    settings_btn = driver.find_element(By.CLASS_NAME,'ytp-settings-button')
    settings_btn.click()
    time.sleep(5)
 
    path_settings = os.path.join(os.path.expanduser("~"), "Imágenes", "settings.png")
    path_settings1 = os.path.join(os.path.expanduser("~"), "Imágenes")
    driver.save_screenshot(path_settings)
    print(f"Captura de la configuración guardada en: { path_settings1 }")
 
    with open(path_settings, "rb") as img_file:
         img_filter_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    html += """
    <h2>Captura del Settings:</h2>
    <img src="data:image/png;base64,""" + img_filter_base64 + """" width="1080"/>
    """
    with open(R_html, "w", encoding="utf-8") as archivo:
      archivo.write(html)
    time.sleep(1)
 
 
    for s in range(10):
         driver.execute_script("window.scrollBy(0, 500)")
         time.sleep(1)
 
    for s in range(10):
         driver.execute_script("window.scrollBy(0, -500)")
         time.sleep(1)

    


def view_youtube_videos(driver):
   
   list_video_btn = driver.find_element(By.XPATH,'//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[2]/div[1]')
   list_video_btn.click()
   time.sleep(2)
   for s in range(4):
        driver.execute_script("window.scrollBy(0, 700)")
        time.sleep(1)

   for s in range(4):
        driver.execute_script("window.scrollBy(0,-700)")
        
  
   list_video_btn = driver.find_element(By.XPATH,'//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[1]')
   list_video_btn.click()
   time.sleep(1)

   view_video = driver.find_element(By.XPATH, '//*[@id="items"]/ytd-grid-video-renderer[1]')
   view_video.click()
   time.sleep(20)  

   #skip_btn = driver.find_element(By.XPATH,'//*[@id="skip-button:2"]')
   #skip_btn.click()

   settings_btn = driver.find_element(By.CLASS_NAME,'ytp-settings-button')
   settings_btn.click()
   time.sleep(5)

   path_settings = os.path.join(os.path.expanduser("~"), "Imágenes", "settings.png")
   path_settings1 = os.path.join(os.path.expanduser("~"), "Imágenes")
   driver.save_screenshot(path_settings)
   print(f"Captura de la configuración guardada en: { path_settings1 }")

   with open(path_settings, "rb") as img_file:
        img_filter_base64 = base64.b64encode(img_file.read()).decode('utf-8')
   html += """
   <h2>Captura del Filtro:</h2>
   <img src="data:image/png;base64,""" + img_filter_base64 + """" width="1080"/>
   """
   with open(R_html, "w", encoding="utf-8") as archivo:
     archivo.write(html)
   time.sleep(1)


   for s in range(10):
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)

   for s in range(10):
        driver.execute_script("window.scrollBy(0, -500)")
        time.sleep(1)
   
        
def filter_videos(driver):
    document = os.path.join(os.path.expanduser("~"), "Documents")
    R_html = os.path.join(document, "Reporte.html")

    html = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de YouTube</title>
        </head>
        <body>
    """
    
    filter_btn = driver.find_element(By.XPATH,'//*[@id="filter-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
    filter_btn.click()
    time.sleep(2)
    path_filter = os.path.join(os.path.expanduser("~"), "Imágenes", "filter.png")
    path_filter1 = os.path.join(os.path.expanduser("~"), "Imágenes")
    driver.save_screenshot(path_filter)
    print(f"Captura de los filtros guardada en: {path_filter1}")
    filte_btn = driver.find_element(By.ID,'close-button')
    filte_btn.click()

    with open(path_filter, "rb") as img_file:
        img_filter_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    html += """
    <h2>Captura del Filtro:</h2>
    <img src="data:image/png;base64,""" + img_filter_base64 + """" width="1080"/>
    """
    with open(R_html, "w", encoding="utf-8") as archivo:
      archivo.write(html)
    time.sleep(1)


def main():
    driver = initialize_driver()


    get_youtube_videos(driver)
   # view_youtube_videos(driver)
    driver.quit()



if __name__ == "__main__":
    main()