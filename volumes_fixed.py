def vol():
    # Вычисление длины интервала по стволу
    depth_min = float(input("Введите нижнюю границу интервала бурения, м: "))
    depth_max = float(input("Введите верхнюю границу интервала бурения, м: "))
    dif_depth = depth_max - depth_min

    # Вычисление нарабатываемого объема бурового раствора
    normal_mud = float(input("Введите норму расхода бурового раствора, м3/м: "))
    volume_accured = normal_mud * dif_depth

    # Вычисление объема бурового раствора
    volume_initial = float(input("Введите объём бурового раствора в обсаженной части скважины, м3: "))

    volume_capacity = float(input("Введите объём рабочих ёмкостей, м3: "))
    volume_mud = volume_capacity + volume_initial + volume_accured

    # Вычисление количества глинопорошка
    normal_clay = float(input("Введите норму расхода глинопорошка, м3/м: "))
    quantity_clay = normal_clay * volume_mud

    # Вычисление количества утяжелителя
    choise = input("Раствор был утяжелён? Y/N: ")
    if choise == 'Y' or choise == 'y':
        # Вычисление коэффициента учитывающего степень повышения плотности
        density_weight = float(input("Введите плотность утяжелителя, кг/м3: "))
        density_initial = float(input("Введите плотность бурового раствор до обработки утяжелителем, кг/м3: "))
        koef_a = (density_weight - density_initial) / 100
        # Потребное количество утяжелителя
        normal_weight = float(input("Введите норму расхода утяжелителя, т/м: "))
        quantity_weight = normal_weight * koef_a * volume_mud
    else:
        quantity_weight = 0

    # Вычисление объемов реагентов
    reagent_array = []  # Массив для вывода
    number_reagent = int(input("Введите количество реагентов: "))
    for i in range(number_reagent):
        reagent_name = input("Введите название: ")
        print("Введите характеристики реагента", reagent_name)
        koef_b = float(input("Понижающий коэффициент при комбинированных обработках (const = 1): "))
        koef_c = float(input("Повышающий коэффициент при дополнительных условиях (const = 1): "))
        normal_reagent = float(input("Норма расхода реагента, т/м3: "))
        quantity_reagent = koef_b * koef_c * normal_reagent * volume_mud
        reagent_array.append([reagent_name, quantity_reagent])

    print("Объем бурового раствора: ", volume_mud, " м3")
    print("Потребное количество глинопорошка: ", quantity_clay, " т")
    print("Потребное утяжелителя: ", quantity_weight, " т")
    print("Потребное количество реагентов: ")
    for reagent in reagent_array:
        print(f"Название: {reagent[0]} - {reagent[1]} т")
