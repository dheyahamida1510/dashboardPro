import json
import re

# membuka file database profile user
with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r") as pd:
    people_data = json.load(pd)

# membuka file template database career
with open("D:\\Dokumen\\dashboardPro\\career_data_temp.json", "r+") as cdf:
    career_data = json.load(cdf)

    # input data nama-nama ke database career
    # iterasi melalui setiap data user
    for p in people_data:
        career_count = 0    # untuk menghitung jumlah data career yang masuk

        # iterasi database career
        for c in career_data:
            i = 0

            # iterasi pada list "career" untuk menemukan kecocokan
            while i < len(c["career"]):

                if re.search(c["career"][i], p["work"], re.IGNORECASE):
                    time_list = []
                    total_time = 0

                    for e in p["experiences"]:
                        cn = 0

                        while cn < len(c["career"]):

                            if re.search(c["career"][cn], e["name"], re.IGNORECASE):
                                
                                # mencari lama waktu tahun
                                yr = 0
                                y = re.search(r"\u00b7\s+(\d+)\s+(yr|yrs?)", e["time"])
                                if y:
                                    yr = int(y.group(1))
                                # ubah tahun ke bentuk bulan
                                yr_to_mos = yr*12

                                # mencari lama waktu bulan
                                mos = 0
                                m = re.search(r"\b(\d+)\s+(mo|mos?)\b", e["time"])
                                if m:
                                    mos = int(m.group(1))

                                # menjumlahkan total waktu
                                total = yr_to_mos + mos
                                time_list.append(total)
                                cn = len(c["career"])
                            cn += 1

                    for tm in time_list:
                        total_time = total_time + tm

                    c["people"].append({"name" : p["name"], "weight" : total_time})
                    c["count"] += 1
                    career_count += 1
                    i = len(c["career"])
                    
                else:
                    exp = 0

                    while exp < len(p["experiences"]):

                        if re.search(c["career"][i], p["experiences"][exp]["name"], re.IGNORECASE):
                            time_list = []
                            total_time = 0

                            for e in p["experiences"]:
                                cn = 0

                                while cn < len(c["career"]):
                                    
                                    if re.search(c["career"][cn], e["name"], re.IGNORECASE):
                                        
                                        # mencari lama waktu tahun
                                        yr = 0
                                        y = re.search(r"\u00b7\s+(\d+)\s+yrs?", e["time"])
                                        if y:
                                            yr = int(y.group(1))
                                        # ubah tahun ke bentuk bulan
                                        yr_to_mos = yr*12

                                        # mencari lama waktu bulan
                                        mos = 0
                                        m = re.search(r"\b(\d+)\s+mos?\b", e["time"])
                                        if m:
                                            mos = int(m.group(1))

                                        # menjumlahkan total waktu
                                        total = yr_to_mos + mos
                                        time_list.append(total)
                                        cn = len(c["career"])
                                    cn += 1

                            for tm in time_list:
                                total_time = total_time + tm

                            c["people"].append({"name" : p["name"], "weight" : total_time})
                            c["count"] += 1
                            career_count += 1
                            i = len(c["career"])
                            exp = len(p["experiences"])

                        exp += 1
                        
                i += 1

        if career_count == 0:
            for c in career_data:
                if c["name"] == "Other":
                    c["people"].append({"name" : p["name"], "weight" : 0})
                    c["count"] += 1
    
    for c in career_data:
        if c["people"]:
            if c["name"] == "Other":
                c["people"].sort(key= lambda x:x["name"].lower())
            else:
                c["people"].sort(key= lambda x:x["weight"], reverse=True)
    
    json_data = json.dumps(career_data, indent=3)

    # membuka dan menulis isi database career
    with open("D:\\Dokumen\\dashboardPro\\career_data.json", "r+") as cd:
        cd.seek(0)
        cd.write(json_data)
        cd.truncate()