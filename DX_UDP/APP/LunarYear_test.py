
from lunar_python import Lunar
 
# 通过指定年月日初始化阴历
lunar = Lunar.fromYmd(1981, 10, 23)
 
# 打印阴历
print(lunar.toFullString())
 
# 阴历转阳历并打印
print(lunar.getSolar().toFullString())