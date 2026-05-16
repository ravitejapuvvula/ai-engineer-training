from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
import datetime
import time

@dataclass
class HelloWorld:

    # variables
    name: str
    age: int

    @property
    def city(self):
        return self.name+ " : ify"
    
    @staticmethod
    def calcuate_dob(age):
        current_date = time.time
        years_ago = datetime.datetime.now() - relativedelta(years=age)
        return str(years_ago)

obj1 = HelloWorld("Ravi",12)
print(HelloWorld.calcuate_dob(12))