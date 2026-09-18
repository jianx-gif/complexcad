import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('YZ',origin=(-87,0,0))
r=w0.sketch().segment((-100,-22),(78,-22)).segment((78,-11)).segment((100,-11)).segment((100,11)).segment((78,11)).segment((78,22)).segment((-100,22)).close().assemble().push([(-56,0)]).circle(6,mode='s').finalize().extrude(-23).union(w1.sketch().segment((-13,-18),(13,-18)).segment((13,18)).segment((-13,18)).segment((-13,11)).segment((6,11)).segment((6,1)).segment((-13,1)).close().assemble().finalize().extrude(151))