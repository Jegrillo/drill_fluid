def density():
    deviant = 20  # Допустимое относительное отклонение
    g = 9.8  # Ускорениие свободного падения

    roof_depth = float(input("Верхняя граница залегающего пласта, м: "))
    depth = float(input("Нижняя граница залегающего пласта, м: "))
    anomaly_coef = float(input(" Коэффициент аномальности: "))
    grad_pres_rock = float(input("Градиент горного давления, МПа/м: "))
    pres_rock = grad_pres_rock * depth  # Горное давление
    grad_pres_pore = float(input("Градиент порового давления, МПа/м: "))
    pres_pore = grad_pres_pore * depth  # Поровое давление
    grad_pres_fracturing = float(input("Градиент давления гидроразрыва, МПа/м: "))
    pres_fracturing = grad_pres_fracturing * depth  # Давление гидроразрыва давление
    unstable_var = input("Наличие неустойчивости горных пород (+/-): ")

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

    output = []
    if (unstable_var == "+"):
        # Расчет реологических параметров: динамическое напряжение сдвига
        dss = 8.5 * density_drill_mud_dep / 1000 - 7
        # Расчет реологических параметров: пластическая вязкость
        plastic_vis = 0.033 * density_drill_mud_dep / 1000 - 0.022
        output.append(density_drill_mud_dep)
    else:
        dss = 8.5 * density_drill_mud_rep / 1000 - 7
        plastic_vis = 0.033 * density_drill_mud_rep / 1000 - 0.022
        output.append(density_drill_mud_rep)

    output.append(dss)
    output.append(plastic_vis)
    return output
