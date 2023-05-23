a = [1,2,57,5]

a.sort(key=lambda x: x.__str__())

print(a)