class Ingredient:
    def __init__(self):
        self.name = []
        self.quantity = []
        self.measurement = None
        self.preparation = []
        self.descriptor = []

    def displayIngredient(self):
        for num in self.quantity:
            print num + ' ',

        if self.measurement is not None:
            print self.measurement + ' ',

        for preparation in self.preparation:
            print preparation + ' ',

        for descriptor in self.descriptor:
            print descriptor + ' ',

        for name in self.name:
            print name + ' ',

        print

    def addPreparation(self, preparation):
        self.preparation.append(preparation)

    def addDescriptor(self, descriptor):
        self.descriptor.append(descriptor)

    def addQuantity(self, quantity):
        self.quantity.append(quantity)

    def addName(self, name):
        self.name.append(name)

    def clearPreparation(self):
        self.preparation = []

    def clearDescriptor(self):
        self.descriptor = []

    def rename(self, newName):
        self.name = []
        self.name.append(newName)
