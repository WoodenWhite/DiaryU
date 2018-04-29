import math
from .models import Pairing


def similityCos(x, y):
    up = x[0]*y[0] + x[1]*y[1] + x[2]*y[2] + x[3]*y[3] + \
        x[4]*y[4] + x[5]*y[5] + x[6]*y[6] + x[7]*y[7]
    down1 = math.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2] + x[3]
                      * x[3] + x[4]*x[4] + x[5]*x[5] + x[6]*x[6] + x[7]*x[7])
    down2 = math.sqrt(y[0]*y[0] + y[1]*y[1] + y[2]*y[2] + y[3]
                      * y[3] + y[4]*y[4] + y[5]*y[5] + y[6]*y[6] + y[7]*y[7])
    return (1.0 * up) / (down1 * down2)


def pair(x, y):  # 两个用户均要存储成功
    x.pair_status = True
    y.pair_status = True
    x.save()
    y.save()
    obj = Pairing(user_one=x, user_two=y)
    obj.save()
    obj = Pairing(user_one=y, user_two=x)
    obj.save()
    obj = Pairing.objects.get(user_one=x)
    tmp_name = obj.id
    obj.pair_name = str(tmp_name)
    obj.save()
    obj = Pairing.objects.get(user_one=y)
    obj.pair_name = str(tmp_name)
    obj.save()


def depair(x):
    obj = Pairing.objects.get(user_one=x)
    y = obj.user_two
    x.pair_status = False
    y.pair_status = False
    x.save()
    y.save()
    Pairing.objects.filter(user_one=x).delete()
    Pairing.objects.filter(user_two=x).delete()
