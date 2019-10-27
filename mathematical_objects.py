from sys import exit

class Matrix():

    def __init__(self, content, m=None, n=None):

        self.validate_arguments(content, m, n)
        self.content = content
        self.m, self.n = self.construct_matrix(m, n)

    def validate_arguments(self, content, m, n):
        if (m and type(m) is not int) or (n and type(n) is not int):
            raise TypeError("Argument types have to be given as following types: Content = list, m = int and n = int.")
        if type(content) is not list:
            raise TypeError("Matrix content has to be given as m lists inside a single list.")
        for x in content:
            if type(x) is list:
                if n and len(x) > n:
                    raise ValueError("If n is given, maximum number of columns is n.")
                for y in x:
                    if type(y) is not int and type(y) is not float:
                        raise TypeError("Matrix cells have to be numbers. One of the element types is" + str(type(y)))
            else:
                raise TypeError("Matrix content has to be given as m lists inside a single list.")
        if m and len(content) > m:
            raise ValueError("If m is given, maximum number of rows is m.")

    def construct_matrix(self, m, n):
        if m:
            rows = m
            if rows > len(self.content):
                for i in range(0, rows - len(self.content)):
                    self.content.append([])
        else:
            rows = len(self.content)
        if n:
            columns = n
        else:
            columns = 1
        for i in range(0, rows):
            x = self.content[i]
            if len(x) > columns:
                columns = len(x)
                i = 0
            elif len(x) < columns:
                for j in range(0, columns - len(x)):
                    x.append(0)
        return rows, columns

    def __str__(self):
        row = ""
        for i in range(0, self.m):
            row += "|"
            row += " ".join(map(str, self.content[i]))
            row += "|\n"
        return row

    def __getitem__(self, index):
        return self.content[index]

    def __setitem__(self, key, value):
        '''if type(value) is list or type(value) is Matrix:
            print("*****ASSIGNING", value[key], "ON", self.content[key])
            self.content[key] = value[key]'''
        if type(value) is int or type(value) is float:
            print("*****ASSIGNING", value[key], "ON", self.content[key])
            self.content[key] = value
        else:
            raise TypeError("Cannot assign " + str(type(value)) + " to matrix.")

    def transpose(self):
        transposed_content = []
        for i in range(0, self.n):
            transposed_content.append([])
            for j in range(0, self.m):
                transposed_content[i].append(self.content[j][i])
        return Matrix(transposed_content)

    def __add__(self, other):
        if type(other) is not Matrix:
            raise TypeError("Matrices can only be added with each other. " +
                            "Type left: " + str(type(self)) + ", type right: " + str(type(other)))
        elif other.m != self.m or other.n != self.n:
            raise ArithmeticError("Addable matrices need to have same dimensions. " +
                            "Dimensions left: " + str(self.m) + "x" + str(self.n) +
                            ", dimensions right: " + str(other.m) + "x" + str(other.n))
        else:
            result_content = []
            for i in range(0, self.m):
                result_content.append([])
                for j in range(0, self.n):
                    result_content[i].append(self[i][j] + other[i][j])
            return Matrix(result_content)

    def __sub__(self, other):
        if type(other) is not Matrix:
            raise TypeError("Matrices can only be subtracted from each other. " +
                            "Type left: " + str(type(self)) + ", type right: " + str(type(other)))
        elif other.m != self.m or other.n != self.n:
            raise ArithmeticError("Subtractable matrices need to have same dimensions. "
                                  "Dimensions left: " + str(self.m) + "x" + str(self.n) +
                                  ", dimensions right: " + str(other.m) + "x" + str(other.n))
        else:
            result_content = []
            for i in range(0, self.m):
                result_content.append([])
                for j in range(0, self.n):
                    result_content[i].append(self[i][j] - other[i][j])
            return Matrix(result_content)

    def __mul__(self, other):
        result_content = []

        # Matrix multiplication
        if type(other) is Matrix:
            if self.n != other.m:
                raise ArithmeticError("Matrix multiplication is only possible if number of columns of the "
                                      "left matrix equals number of rows of the right matrix.\n"
                                      "Dimensions left: " + str(self.m) + "x" + str(self.n) +
                                      ", dimensions right: " + str(other.m) + "x" + str(other.n))
            dot_product = 0
            for a_mi in range(0, self.m):
                result_content.append([])
                for b_ni in range(0, other.n):
                    for i in range(0, self.n):
                        dot_product += self[a_mi][i] * other[i][b_ni]
                    result_content[a_mi].append(dot_product)
                    dot_product = 0
            return Matrix(result_content)

        # Scalar multiplication
        else:
            for i in range(0, self.m):
                result_content.append([])
                for j in range(0, self.n):
                    result_content[i].append(other * self.content[i][j])
        return Matrix(result_content)

    __rmul__ = __mul__

    def __floordiv__(self, other):
        result_content = []
        if type(other) is Matrix:
            raise ArithmeticError("Matrices cannot be divided with each other.")
        elif type(other) == float or type(other) == int:
            for i in range(0, self.m):
                result_content.append([])
                for j in range(0, self.n):
                    result_content[i].append(self.content[i][j] // other)
        return Matrix(result_content)

    def __truediv__(self, other):
        result_content = []
        if type(other) is Matrix:
            raise ArithmeticError("Matrices cannot be divided with each other.")
        elif type(other) == float or type(other) == int:
            for i in range(0, self.m):
                result_content.append([])
                for j in range(0, self.n):
                    result_content[i].append(self.content[i][j] / other )
        return Matrix(result_content)


