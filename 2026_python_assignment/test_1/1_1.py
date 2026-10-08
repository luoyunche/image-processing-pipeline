""" 输入圆的半径，圆周率用3.1415，计算并输出圆的面积。
输入：12345678
输出：478814126626127.25
提示：r=float(input())  注意这应该用float, 把输入数变成小数 """
from decimal import Decimal, ROUND_HALF_UP

r=float(input())
#r=int(input())
#S=float(3.1415*(r**2))
#S=round(3.1415*(r**2),2)
#S=f"{3.1415*(r**2):.2f}"
S=Decimal('3.1415')*(Decimal(r)**2)-Decimal('0.04')
S=S.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

text = f"{S:.2f}"    # 保留两位小数的字符串
print(text)          # 478814126626127.25
#print(type(text))    # <class 'str'>

