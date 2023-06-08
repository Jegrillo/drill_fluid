import math
import density_fixed
import static_shear_stress_fixed
import volumes_fixed

result_1 = density_fixed.density()
density_drill_mud = result_1[0]
dss = result_1[1]
plastic_vis = result_1[2]

# print(density_drill_mud)
result_2 = static_shear_stress_fixed.sns(density_drill_mud, plastic_vis)
sns_60 = result_2[0]
sns_600 = result_2[1]

filtration = 6 * 1000 / density_drill_mud + 3
pH = '8 - 9 pH'

print("Плотность бурового раствора = ", density_drill_mud, " кг/м3")
print("Динамическое напряжение сдвига = ", dss, " Па")
print("Пластическая вязкость = ", plastic_vis, " Па * с")
print("Статическое напряжение сдвига за 1 минуту = ", sns_60, " дПа")
print("Статическое напряжение сдвига за 10 минут = ", sns_600, " дПа")
print("Показатель фильтрации <= ", filtration, " см3 за 30 минут")
print("Уровень фильтрации = ", pH)
volumes_fixed.vol()
