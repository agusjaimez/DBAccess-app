from selenium import webdriver
import re
import time

def search(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver=webdriver.Chrome(options=options)
    driver.get(url)
    nombre=driver.find_element_by_id('hp_hotel_name').get_attribute('textContent')
    ubicacion=driver.find_element_by_xpath('//*[@id="showMap2"]/span[1]').get_attribute('textContent')
    photos_request=driver.find_elements_by_class_name('bh-photo-grid-thumb-cell')
    photo1=driver.find_elements_by_css_selector(".bh-photo-grid-item.bh-photo-grid-photo1.active-image")[0].get_attribute('href')
    photo2=driver.find_elements_by_css_selector(".bh-photo-grid-item.bh-photo-grid-photo2.active-image")[0].get_attribute('href')
    photo3=driver.find_elements_by_css_selector(".bh-photo-grid-item.bh-photo-grid-photo3.active-image")[0].get_attribute('href')
    photos=[photo1,photo2,photo3]
    for i in range(2):
        photos.append(photos_request[i].find_elements_by_tag_name('a')[0].get_attribute('href'))
    try:
        puntuacion=driver.find_elements_by_class_name('bui-review-score__badge')[2].get_attribute('textContent')
        cant_puntuaciones=driver.find_elements_by_class_name('bui-review-score__text')[2].get_attribute('textContent')
    except:
        print('No tiene puntuaciones')
        puntuacion='0,0'
        cant_puntuaciones="0.0 comentarios"
    cant_puntuaciones = re.sub(r'\s|comentarios|\.', '', cant_puntuaciones)
    room_activate=driver.find_elements_by_css_selector('.jqrt.togglelink')
    for i in room_activate:
        i.click()
        time.sleep(2)
        driver.find_elements_by_class_name('lightbox_close_button')[0].click()
    rooms_data=[]
    rooms=driver.find_elements_by_css_selector('.room-lightbox-container.js-async-room-lightbox-container')
    for i in rooms:
        fotos=[]
        facilidades=[]
        for j in range(len(i.find_elements_by_tag_name('div')[1].find_elements_by_css_selector('.hprt-lightbox-gallery-thumbs.hprt-lightbox-gallery-thumbs_border')[0].find_elements_by_tag_name('img'))):
            fotos.append(i.find_elements_by_tag_name('div')[1].find_elements_by_css_selector('.hprt-lightbox-gallery-thumbs.hprt-lightbox-gallery-thumbs_border')[0].find_elements_by_tag_name('img')[j].get_attribute('src'))
        
        for j in range(len(i.find_elements_by_tag_name('div')[1].find_elements_by_class_name('hprt-lightbox-right-container')[0].find_elements_by_css_selector('.hprt-lightbox-list__item.js-lightbox-facility'))):
            facilidades.append(i.find_elements_by_tag_name('div')[1].find_elements_by_class_name('hprt-lightbox-right-container')[0].find_elements_by_css_selector('.hprt-lightbox-list__item.js-lightbox-facility')[j].get_attribute('textContent'))
        room={
            'nombre':i.find_elements_by_xpath(".//*")[1].find_elements_by_tag_name('h1')[0].get_attribute("textContent"),
            'tamaño':re.findall(r'Superficie de la habitación (\d+) m', re.sub(r'\s+', ' ',i.find_elements_by_tag_name('div')[1].find_elements_by_class_name('hprt-lightbox-right-container')[0].get_attribute('textContent'))),
            'fotos':fotos,
            'facilidades': facilidades
        }
        rooms_data.append(room)
    driver.close()
    return {
        'nombre': nombre,
        'ubicacion': ubicacion,
        'fotos1': photos,
        'puntuacion': puntuacion,
        'cant_puntuaciones': cant_puntuaciones,
        'habitaciones': rooms_data
    }


# print(search('https://www.booking.com/hotel/cl/ibis-budget-providencia.html?'))
