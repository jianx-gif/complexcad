import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().arc((37,14),(-40,-6),(39,5)).arc((33,8),(37,14)).assemble().finalize().extrude(4).union(w0.sketch().segment((-23,28),(-18,17)).arc((12,20),(24,-7)).segment((36,1)).segment((15,37)).arc((13,34),(11,33)).segment((11,32)).segment((9,32)).arc((7,32),(5,33)).segment((3,33)).segment((3,34)).arc((-9,35),(-23,28)).assemble().finalize().extrude(14))
