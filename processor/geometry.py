import numpy as np
#import matplotlib.pyplot as plt

# ax + by + c = 0
# a, b, c: coef 0, 1, 2
class Line_2D:
    """
    ax + by + c = 0\n
    a = self.coef[0] and same for b and c\n
    self.angle
    """
    def __init__(self, point1, point2 = None, angle = None):
        if not point2 is None:
            self.get_eq_by2points(point1, point2)
            self._get_angle()
        elif not angle is None:
            self.get_eq_bypointandangle(point1, angle)
            
    def get_eq_by2points(self, point1, point2):
        coef = []
        a = -(point1[1]-point2[1])
        b = point1[0]-point2[0]
        c = -a*point1[0]-b*point1[1]
        normalize_coef = 1/np.sqrt(a**2+b**2)
        coef.append(a*normalize_coef)
        coef.append(b*normalize_coef)
        coef.append(c*normalize_coef)
        self.coef = coef
        
    def get_eq_bypointandangle(self, point, angle):
        a = np.sin(angle)
        b = - np.cos(angle)
        c = -a*point[0]-b*point[1]
        coef = []
        coef.append(a)
        coef.append(b)
        coef.append(c)
        self.coef = coef
    
    def inequality(self, x, y):
        coef = self.coef
        return coef[0]*x+coef[1]*y+coef[2]
    
    def distance(self, x, y):
        coef = self.coef
        d = np.abs(coef[0]*x+coef[1]*y+coef[2]) / np.sqrt(coef[0]**2 + coef[1]**2)
        return d
    
    def intersection_point(self, line):
        L1 = line.coef
        L2 = self.coef
        fraction_coef = L1[1]*L2[0] - L1[0]*L2[1]
        if fraction_coef == 0:
            print("no intersection point of 2 line")
            return np.nan
        y = (L1[0]*L2[2] - L1[2]*L2[0]) / fraction_coef
        x = -(L1[1]*L2[2] - L1[2]*L2[1]) / fraction_coef
        return (x, y)
        
    def _get_angle(self):
        angle = np.arctan2(self.coef[0], (-self.coef[1]))
        # if self.coef[0] == 0:
        #     angle = 0
        # elif self.coef[1] == 0:
        #     angle = 90 / 180 * np.pi
        # else:
        #     angle = np.arctan(self.coef[0] / (-self.coef[1]))
        self.angle = angle
        
def rotation_2D(x, y, angle, rotation_center = [0, 0], angle_type = "radius"):
    if angle_type == "degree":
        angle = angle / 180 * np.pi
    x = x - rotation_center[0]
    y = y - rotation_center[1]
    newx = x * np.cos(angle) - y * np.sin(angle)
    newy = x * np.sin(angle) + y * np.cos(angle)
    newx = newx + rotation_center[0]
    newy = newy + rotation_center[1]
    return newx, newy

def newpoint_by_angle_length(point, angle, length, angle_unit = "radius", angle_type = "math"):
    """
    angle_unit: "radius"("rad") or "degree"("deg")\n
    angle_type: "math" or "met" (metangle = pi/2 - mathangle)
    """
    vectorx, vectory = vector_by_angle_length(angle, length, angle_unit, angle_type)
    return point[0] + vectorx, point[1] + vectory

def vector_by_angle_length(angle, length, angle_unit = "radius", angle_type = "math"):
    """
    angle_unit: "radius"("rad") or "degree"("deg")\n
    angle_type: "math" or "met" (metangle = pi/2 - mathangle)
    """
    if angle_unit in ["deg", "degree"]:
        angle = angle / 180 * np.pi
    if angle_type == "met":
        angle = np.pi/2 - angle
    return length * np.cos(angle), length * np.sin(angle)

class Quadrilaterals:
    def __init__(self, pointlist):
        lines = []
        for ip in range(len(pointlist)):
            lines.append(Line_2D(pointlist[ip-1], pointlist[ip]))
        self.lines = lines
        center_x = sum([p[0] for p in pointlist]) / len(pointlist)
        center_y = sum([p[1] for p in pointlist]) / len(pointlist)
        self.center_point = (center_x, center_y)

    def ifinside(self, x, y):
        boollist = [(line.inequality(x, y) * line.inequality(*self.center_point)) >= 0 for line in self.lines]
        if isinstance(x, np.ndarray):
            result = np.ones_like(x, dtype=bool)
            for b in boollist:
                result *= b
        else:
            result = np.all(np.array(boollist))
        return result

def cubic_eqn(x, a, b, c, d):
    y = a*x**3 + b*x**2 + c*x + d
    return y

def quartic_eqn(x, a, b, c, d, e):
    y = a*x**4 + b*x**3 + c*x**2 + d*x + e
    return y
"""
if __name__ == '__main__':
    x, y = np.meshgrid(np.arange(10), np.arange(20))
    plt.scatter(x,y)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    ax = plt.gca()
    ax.set_aspect('equal', 'box')
    plt.show()
    newx, newy = rotation_2D(x, y, angle = 30, angle_type = "degree", rotation_center = [10, 20])
    plt.scatter(newx,newy)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    ax = plt.gca()
    ax.set_aspect('equal', 'box')
    plt.show()
"""