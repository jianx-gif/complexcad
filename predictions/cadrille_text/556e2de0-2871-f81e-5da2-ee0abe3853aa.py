import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-78,40),(32,-58)).segment((78,-10)).segment((-71,58)).close().assemble().finalize().extrude(200)