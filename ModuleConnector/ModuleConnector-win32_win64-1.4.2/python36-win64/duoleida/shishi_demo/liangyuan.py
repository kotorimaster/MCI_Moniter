import cmath
def ly(r1,r2):
    x=(r2*r2-r1*r1+16)/8
    y=-cmath.sqrt(r2*r2-x*x).real

    return x,y