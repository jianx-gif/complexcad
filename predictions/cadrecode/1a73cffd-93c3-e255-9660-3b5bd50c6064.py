import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
w1=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().segment((-100,-44),(-90,-44)).segment((-90,-42)).segment((-88,-42)).segment((-88,-44)).segment((100,-44)).segment((100,31)).segment((-100,31)).close().assemble().push([(-51,-5)]).circle(6,mode='s').push([(50,-6)]).circle(7,mode='s').finalize().extrude(-25).union(w1.workplane(offset=-48/2).moveTo(0,38).box(12,12,48))