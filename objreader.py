

class Model:
    def __init__(self, filename):
        self.filename = filename
        self.vertices = []  # [[vx, vy, vz]...]
        self.faces = []     # [[[v1, t1, n1], [v2, t2, n2], [v3, t3, n3]]...]
        self.tex = []       # [[u, v]...]
        self.norm = []      # [[nx, ny, nz]...]
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
                if line.startswith('vt '):   # texture coords
                    t = [float(x) for x in data[1:3]]
                    self.tex.append(t)

        print("Read :: ", self.filename)
        print("#vertices = ", len(self.vertices))
        print("#tex coords = ", len(self.tex))
        print("#faces = ", len(self.faces))
