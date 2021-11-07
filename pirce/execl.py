import openpyxl

wb = openpyxl.load_workbook('操作记录.xlsx')
ws = wb['板块强度']
ws['C4'] = 100
wb.save('操作记录1.xlsx')
