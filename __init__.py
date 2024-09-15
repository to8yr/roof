# __init__.py

# Import modules from the package
import math
from .module1 import function1, Class1
from .module2 import function2, Class2

# Expose functions and classes to the package level
__all__ = ['function1', 'Class1', 'function2', 'Class2']

# Add optional package-level variables or functions here
package_variable = "This is a package-level variable"

def package_function():
    print("This is a package-level function")


class reg_duo:
    # initalise regular duoputch
    def __init__(self, lhs=10, rhs=10, length=40, bay_size=2.5, pitch=18, beam_type='D78', build_method='hand'):
        self.lhs = lhs
        self.rhs = rhs
        self.length = length
        self.bay_size = bay_size
        self.pitch = pitch
        self.beam_type = beam_type
        self.build_method = build_method
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)
    
    def integrity(self, weight, wind, snow):
        return weight * wind * snow
    

