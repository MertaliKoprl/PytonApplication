class Dog():
    """Represent a dog."""
    def __init__(self, name):
        """Initialize dog object."""
        self.name = name
    def sit(self):
        """Simulate sitting."""
        print(self.name + " is sitting.")

class SARDog(Dog):
    def __init__(self,name):
        super().__init__(name)

    def search(self):
        print(self.name+ "is searching.")


my_dog = SARDog('Peso')
print(my_dog.name + " is a great dog!")
my_dog.sit()

if(isinstance(my_dog,Dog)):
    print(my_dog.name," is A DOG TOO.")
