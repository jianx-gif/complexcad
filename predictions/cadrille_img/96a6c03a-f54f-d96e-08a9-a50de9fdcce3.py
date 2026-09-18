import cadquery as cq
w0=cq.Workplane('YZ',origin=(21,0,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().push([(0,16)]).circle(84).circle(59,mode='s').finalize().extrude(-83).union(w0.sketch().push([(0,16)]).circle(49).circle(21,mode='s').finalize().extrude(21)).union(w1.sketch().push([(11,10)]).circle(90).circle(80,mode='s').finalize().extrude(-99))