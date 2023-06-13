import openpyxl
import drill_mud_excel

#открытие эксель документа и выбор активного листа
book = openpyxl.load_workbook("data.xlsx")
sheet = book.active

g = 9.8  # Ускорениие свободного падения
row = 5  # Номер первой значимой строки
pos = 1

cur_top = sheet[4][2].value
cur_depth = sheet[4][3].value
cur_pres_plast = sheet[4][8].value
cur_pres_fracturing = sheet[4][7].value

for row in range(5, 13):
    roof_depth = sheet[row][2].value  # Верх залегающего пласта
    depth = sheet[row][3].value  # Низ залегающего пласта
    grad_pres_fracturing = sheet[row][7].value  # Градиент давления гидроразрыва
    grad_pres_plast = sheet[row][8].value  # Градиент пластового давления

    if (grad_pres_plast > cur_pres_plast and cur_pres_plast < grad_pres_fracturing):
        cur_pres_plast = grad_pres_fracturing
    elif (grad_pres_plast > cur_pres_plast and cur_pres_plast >= grad_pres_fracturing):
        drill_mud_excel.import_data2(pos, cur_top, cur_depth, cur_pres_plast, cur_pres_fracturing)
        pos = pos + 1
        cur_top = roof_depth
        cur_depth = depth
        cur_pres_plast = grad_pres_plast
        cur_pres_fracturing = grad_pres_fracturing

    if (grad_pres_fracturing > cur_pres_fracturing and cur_pres_fracturing < grad_pres_plast):
        cur_pres_fracturing = grad_pres_fracturing
    elif (grad_pres_fracturing > cur_pres_fracturing and cur_pres_fracturing <= grad_pres_plast):
        drill_mud_excel.import_data2(pos, cur_top, cur_depth, cur_pres_plast, cur_pres_fracturing)
        pos = pos + 1
        cur_top = roof_depth
        cur_depth = depth
        cur_pres_plast = grad_pres_plast
        cur_pres_fracturing = grad_pres_fracturin

    cur_depth = depth

drill_mud_excel.import_data2(pos, cur_top, cur_depth, cur_pres_plast, cur_pres_fracturing)