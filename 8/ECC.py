class Curve:
    a = 0
    b = 0
    def isValid():
        a = Curve.a
        b = Curve.b
        return 4 * a * a * a + 27 * b * b != 0

class Point(Curve):
    def __init__(self, field, x=None, y=None):
        if x != None:
            self.x = x
        else:
            self.x = int(input("Enter x co-ordinate:"))
        if y != None:
            self.y = y
        else:
            self.y = int(input("Enter y co-ordinate:"))
        self.field = field

    def __add__(self, other):
        if self.field != other.field:
            raise ValueError("Fields of points do not match")
        xd = (other.x - self.x)
        xf = modInverse(xd, self.field)
        slope = (other.y - self.y) * xf
        slope = slope % self.field
        xnew = (slope * slope - self.x - other.x) % self.field
        ynew = (-self.y + slope * (self.x - xnew)) % self.field
        return Point(self.field, xnew, ynew)

    def __neg__(self):
        return Point(self.field, self.x, -self.y % self.field)

    def __str__(self):
        return "({},{}) mod {}".format(self.x, self.y, self.field)

    def __repr__(self):
        return "(x,y) = ({},{}) and field={}".format(self.x, self.y, self.field)

    def __mul__(self, const):
        q = self.double()
        for _ in range(const - 1):
            q = self + q
        return q

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.field == other.field

    def double(self):
        numerator = (3 * self.x * self.x + Curve.a)
        denominator = modInverse(2 * self.y, self.field)
        s = (numerator * denominator) % self.field
        xnew = (s * s - 2 * self.x) % self.field
        ynew = (-self.y + s *(self.x - xnew)) % self.field
        return Point(self.field, xnew, ynew)

    def verify(self):
        lhs = (self.y * self.y) % self.field
        rhs = (self.x * self.x * self.x + Curve.a * self.x + Curve.b) % self.field
        return lhs == rhs
        
def modInverse(a, m) :
    a = a % m;
    for x in range(1, m) :
        if ((a * x) % m == 1) :
            return x
    return 1

if __name__ == "__main__":

    while not Curve.isValid():
        Curve.a = int(input("Enter 'a' of curve: ")) 
        Curve.b = int(input("Enter 'b' of curve: ")) 

    field = int(input("Enter the prime field : "))
    
    repeat = True
    while repeat:
        print("\nOperations:\n\
                0:Generate Keys For Diffie Hellman Keys\n\
                1:Negation of a point\n\
                2:Addition of points\n\
                3:Double a point\n\
                4:Check whether point lies on curve\n\
                5:Exit\n")
        operation = int(input("Enter operation no.: "))
        if operation == 5:
            repeat = False
            continue
        p = Point(field)
        if operation == 0:
            a = int(input("Enter Private Key for Alice:"))
            b = int(input("Enter Private Key for Bob:"))
            KUa = p * a
            KUb = p * b
            s1 = KUa * b
            s2 = KUb * a
            print("Public Key for Alice: " + str(KUa))
            print("Public Key for Bob: " + str(KUb))
            if s1 == s2:
                print("Session key verified: " + str(s1))
            else:
                print("Error:Session keys don't match " + str(s1) + " and " + str(s2))
        elif operation == 1:
            print(-p)
        elif operation == 2:
            print("Second point:")
            q = Point(field)
            r = p + q
            print(r)
        elif operation == 3:
            print(p.double())
        elif operation == 4:
            print("Yes" if p.verify() else "No")
        else:
            print("Invalid input!")
