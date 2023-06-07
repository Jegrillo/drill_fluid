import openpyxl
import drill_mud_excel

#открытие эксель документа и выбор активного листа
book = openpyxl.load_workbook("data.xlsx")
sheet = book.active

deviant = 20  # Допустимое относительное отклонение
g = 9.8  # Ускорениие свободного падения

for row in range (4, 13): # Проход по всем строкам, в которых есть информация
    roof_depth = sheet[row][2].value  # Верх залегающего пласта
    depth = sheet[row][3].value # Низ залегающего пласта
    anomaly_coef = sheet[row][4].value  # Коэффициент аномальности
    grad_pres_rock = sheet[row][5].value  # Градиент горного давления
    pres_rock = grad_pres_rock * depth
    grad_pres_pore = sheet[row][6].value  # Градиент порового давления
    pres_pore = grad_pres_pore * depth
    grad_pres_fracturing = sheet[row][7].value  # Градиент давления гидроразрыва
    pres_fracturing = grad_pres_fracturing * depth
    unstable_var = sheet[row][13].value  # Неустойчивость горных пород (+)
    #print(roof_depth, depth, anomaly_coef, g, unstable_var, k)

    grad_pres_plast = anomaly_coef * g * 1040.0 / 1000000.0  # Градиент пластового давления
    drill_mud_excel.import_data1(row, 9, grad_pres_plast)

    # Пластовое давление
    pres_plast = anomaly_coef * g * 1040.0  * depth / 1000000.0

    # stock_coef = коэффициент запаса относительно глубины бурения
    # pres_rep = допустимая величина репрессии на пласт
    if (roof_depth <= 1200):
        stock_coef = 1.1  # a=[10-15]% Pреп=1.5
        pres_rep = 1.5  # Pреп=1.5 МПа
    elif (roof_depth > 1200 and roof_depth <= 2500):
        stock_coef = 1.05  # a=[5-10]%
        pres_rep = 2.5  # Pреп=2.5 МПа
    else:
        stock_coef = 1.05  # a=[4-7]%
        pres_rep = 3.0  # Pреп=3.0 МПа

    # Если горные породы неустойчивы, плотность бурового раствора при бурении на депрессии
    pres_dep = 0.1 * (pres_rock - pres_pore) # Депрессия на пласт = [10-15]% эффективных скелетных напряжений
    density_drill_mud = (pres_pore + pres_dep) * 1000000 / (g * depth)
    # Ввод расчетной плотности бурового раствора в таблицу
    drill_mud_excel.import_data1(row, 10, density_drill_mud)

    # Плотность бурового раствора, при бурении на репрессии
    pres1 = pres_plast * stock_coef * 1000000 / (g * depth)
    pres2 = (pres_plast + pres_rep) * 1000000 / (g * depth)
    density_drill_mud = min(pres1, pres2)

    #Ввод расчетной плотности бурового раствора в таблицу
    drill_mud_excel.import_data1(row, 11, density_drill_mud)

    #Расчет реологических параметров: динамическое напряжение сдвига
    dss = 8.5 * density_drill_mud / 1000 - 7
    # Расчет реологических параметров: пластическая вязкость
    plastic_vis = 0.033 * density_drill_mud / 1000 - 0.022

    #Ввод реологических параметров в таблицу
    drill_mud_excel.import_data1(row, 12, dss)
    drill_mud_excel.import_data1(row, 13, plastic_vis)
