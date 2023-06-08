import openpyxl
import drill_mud_excel

# Открытие эксель документа и выбор активного листа
book = openpyxl.load_workbook("data.xlsx")
sheet = book.active

deviant = 20  # Допустимое относительное отклонение
g = 9.8  # Ускорениие свободного падения

count_plast = int(input("Введите количество залегающих пластов: "))
choise = int(input("Ввод с клавиатуры - 1 \nВвод с помощью файла ""<data.xlsx>"" - 2 \n"))

if (choise == 1):
    output = []
    for row in range(count_plast):
        name_plast = input("Введите название/индекс залегающего пласта ")
        print("Введите характеристики выбранного пласта ")
        roof_depth = float(input("  Верхняя граница залегающего пласта, м: "))
        depth = float(input("  Нижняя граница залегающего пласта, м: "))
        anomaly_coef = float(input("  Коэффициент аномальности: "))
        grad_pres_rock = float(input("  Градиент горного давления, МПа/м: "))
        pres_rock = grad_pres_rock * depth  # Горное давление
        grad_pres_pore = float(input("  Градиент порового давления, МПа/м: "))
        pres_pore = grad_pres_pore * depth  # Поровое давление
        grad_pres_fracturing = float(input("  Градиент давления гидроразрыва, МПа/м: "))
        pres_fracturing = grad_pres_fracturing * depth  # Давление гидроразрыва давление
        unstable_var = input("  Наличие неустойчивости горных пород (+/-): ")

        grad_pres_plast = anomaly_coef * g * 1040.0 / 1000000.0  # Градиент пластового давления

        # Пластовое давление
        pres_plast = anomaly_coef * g * 1040.0 * depth / 1000000.0

        # stock_coef = коэффициент запаса относительно глубины бурения
        # pres_rep = допустимая величина репрессии на пласт
        if roof_depth <= 1200:
            stock_coef = 1.1  # a=[10-15]% Pреп=1.5
            pres_rep = 1.5  # Pреп=1.5 МПа
        elif (roof_depth > 1200 and roof_depth <= 2500):
            stock_coef = 1.05  # a=[5-10]%
            pres_rep = 2.5  # Pреп=2.5 МПа
        else:
            stock_coef = 1.05  # a=[4-7]%
            pres_rep = 3.0  # Pреп=3.0 МПа

        # Если горные породы неустойчивы, плотность бурового раствора при бурении на депрессии
        pres_dep = 0.1 * (pres_rock - pres_pore)  # Депрессия на пласт = [10-15]% эффективных скелетных напряжений
        density_drill_mud_dep = (pres_pore + pres_dep) * 1000000 / (g * depth)

        # Плотность бурового раствора, при бурении на репрессии
        pres1 = pres_plast * stock_coef * 1000000 / (g * depth)
        pres2 = (pres_plast + pres_rep) * 1000000 / (g * depth)
        density_drill_mud_rep = min(pres1, pres2)

        if (unstable_var == "+"):
            # Расчет реологических параметров: динамическое напряжение сдвига
            dss = 8.5 * density_drill_mud_dep / 1000 - 7
            # Расчет реологических параметров: пластическая вязкость
            plastic_vis = 0.033 * density_drill_mud_dep / 1000 - 0.022
        else:
            dss = 8.5 * density_drill_mud_rep / 1000 - 7
            plastic_vis = 0.033 * density_drill_mud_rep / 1000 - 0.022

        output.append([name_plast, density_drill_mud_dep, density_drill_mud_rep, dss, plastic_vis])

    for reg in output:
        print(f"Название: {reg[0]}. Характеристики бурового раствора:")
        print(f"  Плотность на депрессии: {reg[1]} кг/м3. Плотность на репрессии {reg[2]} кг/м3")
        print(f"Динамическое напряжение сдвига: {reg[3]} Па. Пластическая вязкость: {reg[4]}")

elif (choise == 2):
    for row in range(3, count_plast + 3):  # Проход по всем строкам, в которых есть информация
        roof_depth = sheet[row][3].value  # Верх залегающего пласта
        depth = sheet[row][4].value  # Низ залегающего пласта
        anomaly_coef = sheet[row][5].value  # Коэффициент аномальности
        grad_pres_rock = sheet[row][6].value  # Градиент горного давления
        pres_rock = grad_pres_rock * depth
        grad_pres_pore = sheet[row][7].value  # Градиент порового давления
        pres_pore = grad_pres_pore * depth
        grad_pres_fracturing = sheet[row][8].value  # Градиент давления гидроразрыва
        pres_fracturing = grad_pres_fracturing * depth
        unstable_var = sheet[row][14].value  # Неустойчивость горных пород (+)

        grad_pres_plast = anomaly_coef * g * 1040.0 / 1000000.0  # Градиент пластового давления
        drill_mud_excel.import_data1(row, 10, grad_pres_plast)

        # Пластовое давление
        pres_plast = anomaly_coef * g * 1040.0 * depth / 1000000.0

        # stock_coef = коэффициент запаса относительно глубины бурения
        # pres_rep = допустимая величина репрессии на пласт
        if roof_depth <= 1200:
            stock_coef = 1.1  # a=[10-15]% Pреп=1.5
            pres_rep = 1.5  # Pреп=1.5 МПа
        elif (roof_depth > 1200 and roof_depth <= 2500):
            stock_coef = 1.05  # a=[5-10]%
            pres_rep = 2.5  # Pреп=2.5 МПа
        else:
            stock_coef = 1.05  # a=[4-7]%
            pres_rep = 3.0  # Pреп=3.0 МПа

        # Если горные породы неустойчивы, плотность бурового раствора при бурении на депрессии
        pres_dep = 0.1 * (pres_rock - pres_pore)  # Депрессия на пласт = [10-15]% эффективных скелетных напряжений
        density_drill_mud = (pres_pore + pres_dep) * 1000000 / (g * depth)
        # Ввод расчетной плотности бурового раствора в таблицу
        drill_mud_excel.import_data1(row, 11, density_drill_mud)

        # Плотность бурового раствора, при бурении на репрессии
        pres1 = pres_plast * stock_coef * 1000000 / (g * depth)
        pres2 = (pres_plast + pres_rep) * 1000000 / (g * depth)
        density_drill_mud = min(pres1, pres2)

        # Ввод расчетной плотности бурового раствора в таблицу
        drill_mud_excel.import_data1(row, 12, density_drill_mud)

        # Расчет реологических параметров: динамическое напряжение сдвига
        dss = 8.5 * density_drill_mud / 1000 - 7
        # Расчет реологических параметров: пластическая вязкость
        plastic_vis = 0.033 * density_drill_mud / 1000 - 0.022

        # Ввод реологических параметров в таблицу
        drill_mud_excel.import_data1(row, 13, dss)
        drill_mud_excel.import_data1(row, 14, plastic_vis)

else:
    print("Программа окончилась с ошибкой")
