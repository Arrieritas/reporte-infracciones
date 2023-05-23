import pandas as pd
import numpy as np
from Writer.json import create_json_file
from Writer.excel import write_data
from Constants.buses import buses

def get_data():
    data = pd.read_csv('./Docs/historial_de_eventos.csv', encoding="utf_16", sep='\t', engine='python')
    return data

def get_buses_numbers(data):
    
    buses_numbers = np.unique(
        pd.DataFrame(data.loc[:, "mDescription"]).to_numpy().flatten()
    )
    return buses_numbers

def get_bus_data(data, bus_number):
    bus_filtered = data[data['mDescription'] == bus_number]
    bus_data = pd.DataFrame(bus_filtered.loc[:, ['mDescription', 'eventDescription', 'address', 'gpsDateTime', 'speed', 'driverName']]).to_numpy()
    return bus_data

def get_max_values(bus_data):
    max_values = {}
    last_date = ''
    last_speed = 0
    door_open_speed = 0

    for bus in bus_data:
        date = str(bus[3][0:10])
        bus_number = bus[0]
        event_type = bus[1]
        address = bus[2]
        speed = bus[4]
        driver_name = str(bus[5])
        
        if (date != last_date) and (date not in max_values):
            max_values[date] = {'bus': bus_number, 'placa': buses[str(bus_number)], 'conductor': '', 'vel_max': '', 'puerta_abierta': '', 'ubicacion': ''}
            last_speed = 0
            door_open_speed = 0

        if event_type == 'Exceso de velocidad':
            max_values[date]['vel_max'] = f'{speed} KM/H' if speed >= last_speed else f'{last_speed} KM/H'
            max_values[date]['conductor'] = driver_name
            last_speed = speed if last_speed < speed else last_speed

        if event_type == 'Conduciendo con puerta abierta':
            max_values[date]['puerta_abierta'] = f'SI - {speed} KM/H' if speed > door_open_speed else f'SI - {door_open_speed} KM/H'
            max_values[date]['ubicacion'] = address if speed > door_open_speed else max_values[date]['ubicacion']
            door_open_speed =  speed if door_open_speed < speed else door_open_speed

        last_date = date

    return max_values

def processing_events(data, buses_numbers):
    events_data = {}

    print('Processing...')
    for bus in buses_numbers:
        bus_data = get_bus_data(data, bus)
        max_values = get_max_values(bus_data)
        events_data[bus] = max_values
    print('Process Complete :)')
    return events_data


data = get_data()
buses_numbers = get_buses_numbers(data)
result = processing_events(data, buses_numbers)
create_json_file(result)
write_data(result)

# print(result)