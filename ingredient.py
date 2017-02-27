class Ingredient:
    def __init__(self):
        self.name = []
        self.quantity = []
        self.measurement = None
        self.preparation = []
        self.descriptor = []

    def displayIngredient(self):
        print self.name, self.quantity, self.measurement, self.preparation, self.descriptor

    def addPreparation(self,preparation):
        self.preparation.append(preparation)

    def addDescriptor(self, descriptor):
        self.descriptor.append(descriptor)

    def addQuantity(self, quantity):
        self.quantity.append(quantity)

    def addName(self, name):
        self.name.append(name)
