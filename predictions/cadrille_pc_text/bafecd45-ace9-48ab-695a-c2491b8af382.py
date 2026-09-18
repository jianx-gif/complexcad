import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-100,-49),(100,-49)).segment((100,0)).segment((63,0)).segment((63,49)).segment((62,49)).segment((62,0)).segment((-100,0)).close().assemble().push([(-90,-16)]).circle(1,mode='s').push([(13,-17)]).circle(38,mode='s').finalize().extrude(-20).union(w1.sketch().arc((-53,-75),(-48,-86),(-41,-97)).segment((-41,-75)).close().assemble().finalize().extrude(-122))