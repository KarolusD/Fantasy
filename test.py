class Student:
    def __init__(self):
        self.name = 'Dave'
        self.status = 'Angry'


dave = Student()
# print(list(dave.__dict__.values()))
# print(dir(dave))
# for att in dir(dave):
#     print(att)
n = [1, 2, 3]
print(dir(n))
# attrs = [getattr(dave, att) for att in dir(dave)]
# print(attrs)
