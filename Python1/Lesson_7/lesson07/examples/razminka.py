# coding: utf-8

class BaseClass():
    x = 1
    y = 2

    
class ChildClass(BaseClass):
    x = 111
    y = 222
    
    def mix(BaseClass):
        return BaseClass.y
        
        
c = ChildClass()
print(c.mix())

x = 13
def func():
    x = 1
    class c:
        x = 2
        print(str(x) + ' ' + 'hohoh')
        y = input('y = ')

        def m(self):
            print(str(x) + ' ' + 'm')
    i = c()
    i.m()

print(str(x) + ' ' + 'last')
func()

        




