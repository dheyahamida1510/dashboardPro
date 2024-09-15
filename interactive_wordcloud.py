# memanggil library yang akan digunakan
from dash_holoniq_wordcloud import DashWordcloud
import json

def create_wordcloud():
    # Membukan file database career
    with open("D:\\Dokumen\\dashboardPro\\career_data.json") as cd:
        data = json.load(cd)

    # Inisialisasi list yang akan digunakan pada word cloud
    data_list = []

    # Mengisi list data_list dengan data dari database career
    for c in data:
        people = []
        for p in c["people"]:
            people.append(p["name"])
        worddata = [c["name"], c["count"], c["name"]+" ("+str(c["count"])+")", people]
        data_list.append(worddata)

    # Melakukan perhitungan untuk mengatur ukuran font frasa saaat ditampilkan pada word cloud
    # menentukan ukuran max dan min dari frasa
    size_max = 50
    size_min = 0

    # menentukan value max dari frekuensi frasa (data ke-2 dari setiap list pada data_list)
    value_max = max(data_list, key= lambda x:x[1])[1]

    # menentukan value min dari frekuensi frasa (data ke-2 dari setiap list pada data_list)
    value_min = min(data_list, key= lambda x:x[1])[1]

    # menentukan range dari ukuran font frasa dan frekuensi frasa
    size_range = size_max-size_min
    value_range = value_max-value_min or 1 # range set ke 1 jika hasil perhitungan adalah 0

    # iterasi untuk menentukan ukuran font setiap frasa
    for i in data_list:
        i[1] = int(((i[1] - value_min) / value_range) * size_range + size_min)

    # Membuat word cloud
    wordcloud = DashWordcloud(
        list=data_list,
        color="random-dark",
        backgroundColor="#ffffff",
        width=600, 
        height=400,
        gridSize=16,
        shuffle=True,
        rotateRatio=0.5,
        shrinkToFit=False,
        shape="circle",
        hover=True,
        id="cloud"
    )

    return wordcloud