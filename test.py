from collections import OrderedDict

od = OrderedDict()

od[3] = 3
od[1] = 1
od[4] = 4
od.pop(1)
od[1] = 1
od[5] = {'d':3}
print(tuple(od.items())[3][0])