import density_fixed
import static_shear_stress_fixed
import volumes_fixed

file = open('output.txt', 'w', encoding="utf-8")
#  file.write("Плотность бурового раствора + реологические параметры")
result_1 = density_fixed.density()
density_drill_mud = result_1[0]
dss = result_1[1]
plastic_vis = result_1[2]
print("  Плотность бурового раствора = ", density_drill_mud, " кг/м3")
print("  Динамическое напряжение сдвига = ", dss, " Па")
print("  Пластическая вязкость = ", plastic_vis, " Па * с")
file.write("Плотность бурового раствора = " + str(density_drill_mud) + " кг/м3\n")
file.write("Динамическое напряжение сдвига = " + str(dss) + " Па\n")
file.write("Пластическая вязкость = " + str(plastic_vis) + " Па * с\n")
file.write("Пластическая вязкость = " + str(plastic_vis) + " Па * с\n")

choise = input("Продолжить расчёт параметров? 1/0: ")
if choise != '1':
    file.close()
    exit()

# print(density_drill_mud)
# result_2 = static_shear_stress_fixed.sns(density_drill_mud, plastic_vis)
result_2 = static_shear_stress_fixed.sns(1700, 0.0038)
sns_60 = result_2[0]
sns_600 = result_2[1]

filtration = 6 * 1000 / density_drill_mud + 3
pH = '8 - 9 pH'


print("  Статическое напряжение сдвига за 1 минуту = ", sns_60, " дПа")
print("  Статическое напряжение сдвига за 10 минут = ", sns_600, " дПа")
print("  Показатель фильтрации <= ", filtration, " см3 за 30 минут")
print("  Уровень pH = ", pH)
file.write("Статическое напряжение сдвига за 1 минуту = " + str(sns_60) + " дПа\n")
file.write("Статическое напряжение сдвига за 10 минут = " + str(sns_600) + " дПа\n")
file.write("Показатель фильтрации <= " + str(filtration) + " см3 за 30 минут\n")
file.write("Уровень pH = " + pH + "\n")

choise = input("Продолжить расчёт параметров? 1/0: ")
if choise != '1':
    file.close()
    exit()

result_3 = volumes_fixed.vol()
volume_mud = result_3[0]
file.write("Объем бурового раствора: " + str(volume_mud) + " м3\n")
quantity_clay = result_3[1]
file.write("Потребное количество глинопорошка: " + str(quantity_clay) + " т\n")
quantity_weight = result_3[2]
file.write("Потребное количество утяжелителя: " + str(quantity_weight) + " т\n")
file.write("Потребное количество реагентов: \n")
i = 4
while i < (len(result_3) - 1):
    reagent_name = result_3[i]
    reagent_quanity = result_3[i + 1]
    file.write(str(reagent_name) + " - " + str(reagent_quanity) + "т\n")
    i = i + 2

file.close()
