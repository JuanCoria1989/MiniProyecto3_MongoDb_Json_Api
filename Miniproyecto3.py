import requests
import json
import pymongo


conexion= pymongo.MongoClient("mongodb://localhost:27017")
mydb=conexion['mydatabase']#Selecionamos la base de datos en la cual queremos trabajar


response= requests.get("https://apis.digital.gob.cl/fl/feriados/2020", headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
responseJson=json.loads(response.text)#Lo transforma a JSon

coleccion=mydb['feriados2020']
coleccion.insert_many(responseJson)

print("="*40,"Todos Los Feriados 2020","="*40)
for i in coleccion.find({},{'_id':0,'comentarios':0,'irrenunciable':0,'leyes':0}):
    print("El día de ", i['nombre']+" es un feriado de tipo ", i['tipo']," y se celebra el ",i['fecha'])


print("="*40,"Solo los Feriados Civiles de 2020","="*40)
for i in coleccion.find({'tipo':'Civil'},{'_id':0,'comentarios':0,'irrenunciable':0,'leyes':0}):
    print("El día de ", i['nombre']+" es un feriado de tipo ", i['tipo']," y se celebra el ",i['fecha'])

print("="*40,"Solo los Feriados Irrenunciables de 2020","="*40)
for i in coleccion.find({'irrenunciable':"1"},{'_id':0,'comentarios':0,'irrenunciable':0,'leyes':0}):
    print("El día de ", i['nombre']+" es un feriado de tipo ", i['tipo']," y se celebra el ",i['fecha'])


print("="*40,"Solo los Feriados que incluyen \"Santo\" o \"Santos\"","="*40)
for i in coleccion.find({'nombre':{'$regex':'\w*Santo\w*'}},{'_id':0,'comentarios':0,'irrenunciable':0,'leyes':0}):
    print("El día de ", i['nombre']+" es un feriado de tipo ", i['tipo']," y se celebra el ",i['fecha'])

print("="*40,"Leyes relacionadas con el Plebicito de Abril","="*40)
print("Las leyes involucradas en el día del Plebicito Constitucional son las siguientes:")
for i in coleccion.find({'nombre':'Plebiscito Constitucional'} and {'fecha':{'$regex':'\w*04-26\w*'}},{'_id':0,'comentarios':0,'irrenunciable':0}):
    print("El día de ", i['nombre']+" es un feriado de tipo ", i['tipo']," y se celebra el ",i['fecha'])
    for e in i['leyes']:
        print(e['nombre']," Revisar en: ", e['url'])


