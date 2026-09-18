import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-57))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((24,-58),(33,-58)).segment((33,-51)).arc((29,-55),(24,-58)).assemble().finalize().extrude(114).union(w1.sketch().push([(0,9)]).circle(3).circle(2,mode='s').finalize().extrude(200))