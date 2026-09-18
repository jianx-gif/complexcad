import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-100,-100),(97,-100)).arc((98,-99),(100,-98)).segment((100,-50)).segment((-50,-50)).segment((-50,97)).segment((-51,97)).segment((-51,100)).segment((-100,100)).close().assemble().push([(51,-72)]).circle(2,mode='s').push([(69,-68)]).circle(5,mode='s').finalize().extrude(-20)