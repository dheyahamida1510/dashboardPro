# memanggil library yang akan digunakan
from dash_holoniq_wordcloud import DashWordcloud
import json

def create_wordcloud():
    with open("D:\\Dokumen\\career_data.json") as cd:
        data = json.load(cd)

    data_list = []

    for c in data:
        worddata = [c["name"], c["count"], c["name"]+" ("+str(c["count"])+")", c["people"]]
        data_list.append(worddata)

    # Melakukan perhitungan untuk mengatur ukuran font frasa saaat ditampilkan pada word cloud
    size_max = 50
    size_min = 0
    value_max = max(data_list, key= lambda x:x[1])[1]
    value_min = min(data_list, key= lambda x:x[1])[1]
    size_range = size_max-size_min
    value_range = value_max-value_min or 1
    for i in data_list:
        i[1] = int(((i[1] - value_min) / value_range) * size_range + size_min)

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