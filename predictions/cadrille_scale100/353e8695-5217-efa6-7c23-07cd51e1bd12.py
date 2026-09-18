import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((12,-28),(13,-27),(15,-26)).arc((-14,27),(12,-28)).assemble().push([(0,1)]).circle(24,mode='s').finalize().extrude(40).union(w0.sketch().push([(0,1)]).circle(29).circle(24,mode='s').finalize().extrude(40))