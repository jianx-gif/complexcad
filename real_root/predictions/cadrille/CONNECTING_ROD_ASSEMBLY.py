import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,19,0))
w1=cq.Workplane('YZ',origin=(-42,0,0))
r=w0.sketch().push([(0,-59)]).circle(28).circle(22,mode='s').finalize().extrude(-38).union(w0.sketch().push([(0,-59)]).circle(23).circle(21,mode='s').push([(0,88)]).circle(12).circle(8,mode='s').finalize().extrude(-31)).union(w1.sketch().push([(0,-1)]).circle(11).circle(3,mode='s').finalize().extrude(133))