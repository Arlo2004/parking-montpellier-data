import pandas as pd
import matplotlib.pyplot as plt
archivo ="parkings_montpellier.csv"
data= pd.read_csv(archivo) 

print("Leyendo los datos....[...]")

data["fecha_lectura"] =pd.to_datetime(data["fecha_lectura"])
data["capacidad_total"]= pd.to_numeric(data["capacidad_total"], errors ="coerce")
data["plazas_libres"]=pd.to_numeric(data["plazas_libres"], errors= "coerce")
data = data.dropna()# X filas vacias

listcenter = ["Comedie","Corum", "Foch","Triangle", "Arc de Triomphe", "Pitot", "Gambetta"]
data_centro = data[data["nombre_parking"].isin(listcenter)] #Filtro centro

data_centro["dia_s"]= data_centro["fecha_lectura"].dt.date
data_centro["hora"]= data_centro["fecha_lectura"].dt.hour
data_centro["minuto"]=data_centro["fecha_lectura"].dt.minute
data_centro["tiempo_x"] = data_centro["hora"] + (data_centro["minuto"] / 60) #horas decimaless

tabla_final = data_centro.groupby(["dia_s", "fecha_lectura", "tiempo_x"]).sum().reset_index() #agrupation


ocupadas = tabla_final["capacidad_total"] - tabla_final["plazas_libres"] #formula
tabla_final["porcentaje%"]= (ocupadas/tabla_final[ "capacidad_total" ]) *100

#Grafico estadistica
plt.figure(figsize=(10, 5))
dias_dis = tabla_final["dia_s"].unique()

for d in dias_dis:
    dato_hoy = tabla_final[tabla_final["dia_s"]== d] #filtro
    plt.plot(dato_hoy["tiempo_x"], dato_hoy["porcentaje%"], label=str(d)) #lineas
#estetica ///

plt.title("--Occupation des parkings dans le centre de Montpellier--")
plt.xlabel("Temps Hs:")
plt.ylabel("occupation %")
plt.ylim(0,100)
plt.xlim(0, 24)
plt.grid(True)
plt.legend()
plt.xticks(range(0, 25, 2), [f"{i:02d}:00" for i in range(0, 25, 2)]) #00:00 02:00 04:00 etc.
plt.grid(True,alpha=0.3) 
plt.legend()
plt.savefig("Grafico-parking-ville-montpellier.png") #end
print("Listo, grafico guardado")
plt.show()
