import json
from datetime import date, timedelta

with open("dataWanted.json") as f:
    data = json.load(f)

start_date = date(2020, 4, 3)
end_date = date(2020, 10, 14)
delta = timedelta(days=1)
i = 0
lista_judete = ["AB", "AR", "AG", "B", "BC", "BH", "BN", "BT", "BV", "BR", "BZ", "CS", "CL", "CJ", "CT", "CV", "DB", "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SM", "SJ", "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"]
o = open("de_trimis.txt", "a")
while(start_date <= end_date):
    start_date += delta
    actual_date = date(2020, 4, 3)
    data_date = actual_date.strftime("%Y-%m-%d")
    o.write(lista_judete[i])
    o.write("-")
    o.flush()
    while(actual_date <= end_date):
        # print(data[data_date][lista_judete[i]])
        # print(lista_judete[i], data[str(actual_date)][lista_judete[i]])
        o.write(str(data[str(actual_date)][lista_judete[i]]))
        o.flush()
        o.write(" ")
        actual_date += delta
    i += 1
    
