
from lunar_python import Lunar, Solar
 
# 通过指定年月日初始化阳历
solar = Solar.fromYmd(1981, 10, 23)

# 通过指定年月日初始化阴历
# lunar = Lunar.fromYmd(1981, 11, 19)
lunar = solar.getLunar()
 
# 打印阴历
print(lunar.toFullString())
 
# 阴历转阳历并打印
print(lunar.getSolar().toFullString())