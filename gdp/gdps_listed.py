#SAYILARIN DUZENLENMESI LAZIM ONUN DISINDA TAMAM

import pandas
import folium
import eel
import folium.plugins 
#import webview
#from sys import exit

#GDP
veri = pandas.read_excel(r"C:\Users\Gorkem\Desktop\GitHub Uploads\gdp_project_file\gdp\gdps_listed.xlsx")

#GDP Excel Labels
enlemler       = list(veri["Enlem"])
boylamlar      = list(veri["Boylam"])
son_yil_gdp    = list(veri["Son"])
onceki_yil_gdp = list(veri["Önceki"])
gdp_fark       = list(veri["Son - Önceki GDP"])
nufus          = list(veri["Nüfus"])



son_yil_gdp_haritasi = folium.FeatureGroup(name = "Güncel GDP Haritası Harita (USD BILLION)", show = False) #harita katmani, butonlarin eklenisi, katman ismi
onceki_yil_gdp_haritasi = folium.FeatureGroup(name = "Referans Yılı GDP Haritasi (USD BILLION)", show = False)
fark_gdp_haritasi = folium.FeatureGroup(name = "Güncel ve Referans Yılı GDP Farkı Haritasi (USD BILLION)", show = False)
nufus_dagilim_haritasi = folium.FeatureGroup(name = "Nüfus Dağılım Haritası (Main Layer)", control = False)



def son_yil_gdp_renk(son_gdp): #returns string, renk girisi
    if son_gdp   >= 10000:
        return "green"
    elif 100 < son_gdp < 10:
        return "white"
    elif 10 < son_gdp < 0:
        return "orange"
    else:
        return "red"

def son_yil_gdp_radius(son_gdp): #returns int, daire yaricapi, daire buyuklugu
    if son_gdp > 10000:
        return 800000
    elif son_gdp > 50000:
        return 400000
    elif son_gdp > 700:
        return 200000
    else:
        return 90000



def onceki_yil_gdp_renk(onceki_gdp):
    if onceki_gdp   >= 10000:
        return "green"
    elif 10000 < onceki_gdp < 10:
        return "white"
    elif 10 < onceki_gdp < 0:
        return "orange"
    else:
        return "red"

def onceki_yil_gdp_radius(onceki_gdp):
    if onceki_gdp > 10000:
        return 800000
    elif onceki_gdp > 50000:
        return 400000
    elif onceki_gdp > 700:
        return 200000
    else:
        return 90000



def fark_gdp_renk(onceki_gdp, son_gdp):
    if son_gdp - onceki_gdp >= 150:
        return "green"
    elif 150 < son_gdp - onceki_gdp <= 0:
        return "white"
    elif 0 < son_gdp - onceki_gdp < -50:
        return "orange"
    else:
        return "red"

def fark_gdp_radius(onceki_gdp, son_gdp):
    if son_gdp - onceki_gdp >= 150:
        return 400000
    elif 150 < son_gdp - onceki_gdp < 0 :
        return 200000
    elif 0 <= son_gdp - onceki_gdp < -50:
        return 100000
    else:
        return 90000




world_map = folium.Map(zoom_start = 4, tiles = "Cartodb dark_matter") # haritanin olusturulmasi




for enlem, boylam, son_gdp in zip(enlemler, boylamlar, son_yil_gdp): #harita degerlerinin ayarlanmasi
    son_yil_gdp_haritasi.add_child(folium.Circle(location = (enlem, boylam),
                                        radius = son_yil_gdp_radius(son_gdp),
                                        color = son_yil_gdp_renk(son_gdp), 
                                        fill_color = son_yil_gdp_renk(son_gdp),
                                        fill_opacity = 0.3))

for enlem, boylam, onceki_gdp in zip(enlemler, boylamlar, onceki_yil_gdp): #harita degerlerinin ayarlanmasi
    onceki_yil_gdp_haritasi.add_child(folium.Circle(location = (enlem, boylam),
                                        radius = onceki_yil_gdp_radius(onceki_gdp),
                                        color = onceki_yil_gdp_renk(onceki_gdp), 
                                        fill_color = onceki_yil_gdp_renk(onceki_gdp),
                                        fill_opacity = 0.3))

for enlem, boylam, onceki_gdp, son_gdp in zip(enlemler, boylamlar, onceki_yil_gdp, son_yil_gdp): #harita degerlerinin ayarlanmasi
    fark_gdp_haritasi.add_child(folium.Circle(location = (enlem, boylam),
                                        radius = fark_gdp_radius(onceki_gdp, son_gdp),
                                        color = fark_gdp_renk(onceki_gdp, son_gdp), 
                                        fill_color = fark_gdp_renk(onceki_gdp, son_gdp),
                                        fill_opacity = 0.3))




#Ulke sinirlarinin cizilmesi
nufus_dagilim_haritasi.add_child(folium.GeoJson(data = (open(r"C:\Users\Gorkem\Desktop\GitHub Uploads\gdp_project_file\gdp\world.json", "r", encoding = "utf-8-sig").read()),
                                        style_function = lambda x :{"fillColor": "red" if x["properties"]["POP2005"] > 100000000 else "orange",
                                        "color" : "white", "weight" : 0.75},
                                        highlight_function = lambda x :{"fillColor": "black"}, ))




world_map.add_child(son_yil_gdp_haritasi)
world_map.add_child(onceki_yil_gdp_haritasi)
world_map.add_child(fark_gdp_haritasi)
world_map.add_child(nufus_dagilim_haritasi)



world_map.add_child(folium.LayerControl()) #buton fonksiyonu
world_map.add_child(folium.LatLngPopup()) #
world_map.add_child(folium.plugins.Geocoder(position="topleft"))
world_map.add_child(folium.plugins.Fullscreen(position="topright", title="Expand", title_cancel="Exit Expanded View", force_separate_button=True))
world_map.add_child(folium.plugins.MiniMap(toggle_display=True, show = True, zoom_level_offset=-12))

world_map.save("world_map_gdp.html") #html olarak kayit 


#Window View
if __name__ == '__main__':
    eel.init(".")
    eel.start(r"C:\Users\Gorkem\Desktop\GitHub Uploads\gdp_project_file\gdp\world_map_gdp.html")
    #eel._detect_shutdown()
    #webview.create_window("Title", "WorldMapDataDisplay", frameless = True)
    #webview.start() 






