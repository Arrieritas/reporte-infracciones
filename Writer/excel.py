from openpyxl import Workbook
from Processor.excel import generate_excel_list

def write_data(data):
    print('Writing...')
    wb = Workbook()
    ws = wb.create_sheet("ABRIL")

    list = generate_excel_list(data)

    for row in list:
        ws.append(row)
    

    wb.save('./Output/reporte.xlsx')
    
    print('Complete :)')