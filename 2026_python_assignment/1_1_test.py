'''from decimal import Decimal, ROUND_HALF_UP

r = int(input())
S = Decimal('3.1415') * (Decimal(r) ** 2)
print("原始 =", S)
S = S.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print("最终 =", S)'''

'''from decimal import Decimal
d = Decimal('3.1415')
print("d =", repr(d))
print("r2 =", repr(Decimal(12345678) ** 2))
print("d * r2 =", repr(d * Decimal(12345678) ** 2))
print([hex(ord(c)) for c in '3.1415'])'''

'''r = float(input())
S = 3.1415 * (r ** 2)
print(S)'''


r = float(input())
pi = 3.1415
area = pi * r * r
print(area)
