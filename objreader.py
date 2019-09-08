

class Model:
    def __init__(self, filename):
        self.filename = filename
        self.vertices = []
        self.faces = []
        self.__read()

    def __read(self):
        with open(self.filename, 'r') as file:
            for line in file:
                data = line.split()
                if line.startswith('v '):   # vertex
                    v = [float(x) for x in data[1:]]
                    self.vertices.append(v)
                if line.startswith('f '):   # face
                    f = [[int(i) - 1 for i in x.split('/')] for x in data[1:]]
                    self.faces.append(f)

        print("Read :: ", self.filename)
        print("#vertices = ", len(self.vertices))
        print("#faces = ", len(self.faces))
