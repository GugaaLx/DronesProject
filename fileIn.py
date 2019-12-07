# 2019-2020 Programação 1 (LTI)
# Grupo N
# número nome
# número nome
import datetime
import pprint

pprint = pprint.PrettyPrinter().pprint

# recebe o ficheiro ja aberto
# (para nao abrir duas vezes)
# e devolve os dados lidos no cabecalho

def readHeader(fileIn):
    fileIn.readline()
    time_str = fileIn.readline().replace("\n", "")
    fileIn.readline()
    date_str = fileIn.readline().replace("\n", "")
    dt = datetime.datetime.strptime(date_str + " " + time_str, "%d-%m-%Y %Hh%M")
    fileIn.readline()
    company = fileIn.readline().replace("\n", "")
    fileIn.readline()
    return [dt, company]

'''
INSERE ORDENADAMENTE (por datetime) item em location_list
location_list - a lista de items na qual vamos inserir o segundo argumento
item - o objecto que saiu ou do processDrone ou do processParcel, ou seja
uma lista tipificada cujo primeiro elemento e um datetime
'''
def list_insert(lista, item):
    i = 0
    while i < len(lista) and lista[i][0] < item[0]:
        i += 1
    lista = lista[:i] + [item] + lista[i:]
    return lista


parcels = []

# constantes das parcels (out parcel)
op_datetime = 0
op_client_name = 1
op_location = 2
op_base_distance = 3
op_weight = 4
op_time_needed = 5


def processParcel(item):
    idt = datetime.datetime.strptime(item[2].strip() + " " + item[3], "%Y-%m-%d %H:%M")
    delta = datetime.timedelta(minutes=int(item[6]))
    parcel = [idt, item[0], item[1], int(item[4]), int(item[5]), delta]
    return parcel


def readParcelsFile(fileName):
    global parcels
    fileIn = open(fileName, 'r')
    [dt, company] = readHeader(fileIn)
    for line in fileIn:
        item = line.replace("\n", "").split(', ')
        parcels = list_insert(parcels, processParcel(item))
    fileIn.close()
    return [dt, company]


def dict_insert(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = list_insert(dictionary[key], value)
    else:
        dictionary[key] = [value]


drone_dict = {}

# constantes drones (out drone)
od_datetime = op_datetime
od_name = 1
od_max_weight = 2
od_max_distance = 3
od_acum_distance = 4
od_battery_life = 5

'''
esta funcao recebe uma lista de strings referente a um drone no formato
[nome, localizacao, peso, distancia maxima, distancia acumulada, autonomia, data, hora]
e devolve uma lista no formato
[DateTime: data e hora, string: nome, int: peso,
int: distancia maxma, float: distancia acumulada, float: autonomia]
'''

def processDrone(item):
    idt = datetime.datetime.strptime(item[6] + " " + item[7], "%Y-%m-%d %H:%M")
    drone = [idt, item[0], int(item[2]), int(item[3]), float(item[4]), float(item[5])]
    return drone


def readDronesFile(fileName):
    fileIn = open(fileName, 'r')
    [dt, company] = readHeader(fileIn)
    for line in fileIn:
        if line.strip() == "":
            continue
        item = line.replace("\n", "").split(', ')
        real_item = processDrone(item)
        dict_insert(drone_dict, item[1], real_item)
    fileIn.close()
    return [dt, company]


def output(parcel, status):
        dt = parcel[op_datetime]
        print(dt.strftime("%Y-%m-%d, %H:%M") + ", " + parcel[op_client_name] + ", " + status)


def parcel_cancel(parcel):
    output(parcel, "cancelled")


def drone_deliver(drone, parcel):
    output(parcel, drone[od_name])
    # modificar drone
    drone[od_datetime] += parcel[op_time_needed]


def drone_can(drone, parcel):
    if drone[od_max_weight] < parcel[op_weight]:
        return False

    if parcel[op_base_distance] * 2 > drone[od_battery_life] * 1000:
        return False

    return True


print(readDronesFile('TestSet1/drones11h00_2019y11m5.txt'))
print(readParcelsFile('TestSet1/parcels11h00_2019y11m5.txt'))

for parcel in parcels:
    location_name = parcel[op_location]
    if location_name in drone_dict:
        drones_list = drone_dict[location_name]

        i = 0
        l = len(drones_list)
        while i < l and not drone_can(drones_list[i], parcel):
            i += 1

        if i == l:
            parcel_cancel(parcel)

        else:
            drone = drones_list.pop(i)
            drone_deliver(drone, parcel)
            drones_list = list_insert(drones_list, drone)

    else:
        parcel_cancel(parcel)
