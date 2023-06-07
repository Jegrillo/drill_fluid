import math

g = 980 # Ускорение свободного падения см / с2

#Ввод параметров, ранее известных
density_drill_mud = float(input("Введите плотность бурового раствора, кг/м3: "))
density_drill_mud = density_drill_mud / 1000  # При расчете используется плотность в т/м3
plastic_vis = float(input("Введите пластическую вязкость, Па*с (Н/с*м2): "))
plastic_vis = plastic_vis * 10 # При расчете используется плотность в Пуаз (г/cм*с)

#Ввод неизвестных параметров

#Определение поперечного размера частиц шлама, см
bit_diameter = float(input("Введите диаметр долота: "))
bit_type = int(input("1 - шарошечное долото с фрезерованными зубьями \n" 
                     "2 - шарошечное долото c зубковым вооружением \n" 
                     "3 - алмазное долото \n"
                     "4 - зубковое долото \n"
                     "5 - долото истерающе-режущего типа \n"
                     "6 - долото типа Т, ТК, К, ОК, ИСМ, АБИ или с буквой З \n"
                     "Введите тип долота: "))
if (bit_type == 1):
    sludge_particle_size = 0.35 + 0.037 * bit_diameter
elif (bit_type == 2 or bit_type == 3):
    sludge_particle_size = 0.25 + 0.035 * bit_diameter
elif (bit_type == 4 or bit_type == 5):
    sludge_particle_size = 0.2 + 0.035 * bit_diameter
elif (bit_type == 6):
    sludge_particle_size = 0.25 + 0.025 * bit_diameter

#Определение минимального касательного напряжения для удержания частиц выбуренной породы, дПа
density_rock = float(input("Введите плотность горной породы, кг/м3: "))
density_rock = density_rock / 1000 # При расчете используется плотность в т/м3
koef_m = float(input("Введите коэффициент формы, зависящий от формы частиц выбуренной породы: "))
shear_stress_min =  sludge_particle_size * (density_rock - density_drill_mud) * g / (6 * koef_m)

#Определение внутреннего диаметра обсадной колонны, м
column_diameter_outer = float(input("Введите наружный диаметр обсадной колонны, мм: "))
column_diameter_outer = column_diameter_outer / 1000 # При расчете используется плотность в м
column_wall_thickness = float(input("Введите толщину стенки обсадной трубы, мм (9, если не указано иной): "))
column_wall_thickness = column_wall_thickness / 1000 # При расчете используется плотность в м
column_diameter_inner = column_diameter_outer - 2 * column_wall_thickness

#Определение объема раствора в обсаженной части скважины, м3
depth_casing = float(input("Введите глубину спуска предыдущей обсадной колонны, м: "))
volume_mud_cased = 0.785 * (column_diameter_inner ** 2) * depth_casing

#Определение объема выбуренной породы, м3
koef_kav = float(input("Введите коэффициент кавернозности: "))
depth_drilling = float(input("Введите глубину бурения выбранным диаметром долота, м: "))
volume_rock = 0.785 * koef_kav * (bit_diameter ** 2) * (depth_drilling - depth_casing)

#Определение объема циркулирующего раствора, м3
volume_mud = volume_mud_cased + volume_rock

#Определение концентрации выбуренной породы в объёме раствора
clean_num_stage = float(input("Введите количество ступеней очистки (I - IV): "))
clean_mud_degree = float(input("Введите степень очистки (0,3 - 0,9): "))
concentration_rock = volume_rock * (1 - clean_mud_degree) / (2 * volume_mud)

#Определение расчетного коэффициента B для удержания частиц выбуренной породы
avg_size_rock = float(input("Введите средний размер частиц выбуренной породы, см: "))
koef_b = 1 / (1 + 0.034 * ((avg_size_rock ** 1.5) / plastic_vis ) * \
        ((density_drill_mud * (density_rock - density_drill_mud) * g) ** 0.5))
print(koef_b)

#Если раствор утяжелен
choise = input("Раствор был утяжелён? Y/N:")
if (choise == 'Y' or choise == 'y'):
    #Определение концентрации утяжелителя в объеме раствора
    density_weight = float(input("Введите плотность утяжелителя, кг/м3: "))
    density_weight = density_weight / 1000  # При расчете используется плотность в т/м3
    density_initial = float(input("Введите плотность бурового раствор до обработки утяжелителем, кг/м3: "))
    density_initial = density_initial / 1000  # При расчете используется плотность в т/м3
    concentration_weight = (density_drill_mud - density_initial) / (density_weight - density_initial)

    # Определение максимального размера частиц утяжелителя, удерживающихся во взвешенном состоянии при мин СНС, см
    koef_m_weight = float(input("Введите коэффициент формы частиц утяжелителя (табличное - 1.8-2): "))
    weight_size_max = 6 * koef_m_weight * shear_stress_min / ((density_weight - density_drill_mud) * g)

    # Вычисление коэффициента k для утяжеленного раствора
    avg_size_weight = float(input("Введите средний размер частиц утяжелителя, см: "))
    koef_k_weight = ((0.0667 * koef_m_weight * concentration_weight * avg_size_weight * shear_stress_min) / \
                    (6 * plastic_vis)) * ((density_weight - density_drill_mud) - 1) * \
                    (math.log(weight_size_max / (weight_size_max - avg_size_weight)) - \
                    avg_size_weight / weight_size_max)
else:
    koef_k_weight = 0

# Вычисление коэффициента k
avg_size_rock = float(input("Введите средний размер частиц выбуренной породы, см: "))
concentration_rock_bottom = float(input("Введите значение объемной концентрации выбуренной породы в осадке \n"
                                        "на забое скважины (0.5-0.85). Для расчетов - 0.7: "))
sediment_heigth_bottom = float(input("Введите высоту осадка на забое (50-300). Для расчетов - 100, см: "))
koef_k = (koef_m * shear_stress_min * concentration_rock * avg_size_rock * koef_b / \
         (3 * plastic_vis * concentration_rock_bottom * sediment_heigth_bottom)) * \
         (math.log(1 - avg_size_rock / sludge_particle_size) + avg_size_rock / sludge_particle_size)
koef_k = koef_k * (-1)

# Принимаем за расчетный коэффициент k больший из двух вычисленных коэффициентов
koef_k = max(koef_k_weight, koef_k)

# Вычисление статического напряжения сдвига в течение 1 минуты и 10 минут, дПа
sns_60 = shear_stress_min * koef_k * 60 / (1 + koef_k * 60)
sns_600 = shear_stress_min * koef_k * 600 / (1 + koef_k * 600)

print("Статическое напряжение в течение 1 минуты: ", sns_60)
print("Статическое напряжение в течение 10 минут: ", sns_600)