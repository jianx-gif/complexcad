import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((24,-81),(24,-70)).arc((-73,0),(24,70)).segment((24,81)).arc((-100,0),(24,-81)).assemble().finalize().extrude(40).union(w1.sketch().push([(0,11)]).circle(89).circle(58,mode='s').finalize().extrude(200))