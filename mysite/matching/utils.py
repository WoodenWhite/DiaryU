import math


def similityCos(x, y):
    up = x[0]*y[0] + x[1]*y[1] + x[2]*y[2] + x[3]*y[3] + \
        x[4]*y[4] + x[5]*y[5] + x[6]*y[6] + x[7]*y[7]
    down1 = math.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2] + x[3]
                      * x[3] + x[4]*x[4] + x[5]*x[5] + x[6]*x[6] + x[7]*x[7])
    down2 = math.sqrt(y[0]*y[0] + y[1]*y[1] + y[2]*y[2] + y[3]
                      * y[3] + y[4]*y[4] + y[5]*y[5] + y[6]*y[6] + y[7]*y[7])
    return (1.0 * up) / (down1 * down2)
