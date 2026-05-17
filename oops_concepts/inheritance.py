from abc import ABC,abstractmethod

class BaseClass(ABC):
    def __init__(self,name,age) -> None:
        self.name= name
        self.age=age

    @abstractmethod
    def import_mandatory(self,name):
        self.full_name = self.name + ". teja"
        return self.full_name, self.age+10
    

class SubClass(BaseClass):

    def import_mandatory(self, name):
        return super().import_mandatory(name)


obj1 = SubClass(name='Sai',age=12)

full_name, age = obj1.import_mandatory(name='Sai')

print("Full name : " + full_name + age)