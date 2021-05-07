import cmath
def ly(r1,r2):
    x=(r1*r1-r2*r2+16)/8
    y=cmath.sqrt(r1*r1-x*x).real

    return x,y