import cadquery as cq
w0=cq.Workplane('YZ',origin=(-77,0,0))
w1=cq.Workplane('ZX',origin=(0,-21,0))
r=w0.sketch().circle(74).reset().face(w0.sketch().segment((-68,11),(-33,-58)).segment((68,-11)).segment((33,58)).close().assemble(),mode='s').finalize().extrude(154).union(w1.sketch().circle(100).circle(91,mode='s').finalize().extrude(29))