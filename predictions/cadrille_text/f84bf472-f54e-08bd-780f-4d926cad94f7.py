import cadquery as cq
w0=cq.Workplane('XY',origin=(-70,0,-100))
w1=cq.Workplane('XY',origin=(-20,0,-100))
r=w0.sketch().segment((-70,77),(-69,77)).segment((-69,79)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(20,0)]).circle(80).circle(57,mode='s').finalize().extrude(110))