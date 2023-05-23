def generate_excel_list (dict:dict):
    excel_list = [
        ['FECHA', 'VEHICULO', 'PLACA', 'CONDUCTOR', 'VELOCIDAD MAXIMA DIA', 'CONDUCIR CON PUERTA ABIERTA', 'UBICACION', 'CIERRE DE VIAJES', 'ABANDONO DE RUTA', 'REPORTE DE NOVEDADES']
    ]


    for key, value in dict.items():
        for k, v in value.items():
            excel_list.append([
                k,
                v['bus'],
                v['placa'],
                v['conductor'],
                v['vel_max'],
                v['puerta_abierta'],
                v['ubicacion'],
                '',
                '',
                ''
                ])

    return excel_list