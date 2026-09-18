import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().arc((-39,10),(38,-13),(-38,13)).arc((-38,11),(-39,10)).assemble().push([(0,0)]).circle(35,mode='s').finalize().extrude(-15).union(w0.sketch().push([(0,0)]).circle(40).circle(12,mode='s').finalize().extrude(-5))
