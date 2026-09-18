import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('XY',origin=(0,0,-5))
r=w0.sketch().segment((-67,-5),(-66,-5)).segment((-66,-22)).segment((67,-10)).segment((67,22)).segment((-67,22)).close().assemble().push([(-28,4)]).circle(6,mode='s').push([(30,8)]).circle(2,mode='s').finalize().extrude(200).union(w1.sketch().arc((-96,28),(66,-75),(-51,86)).arc((-11,-10),(-96,28)).assemble().finalize().extrude(-16))