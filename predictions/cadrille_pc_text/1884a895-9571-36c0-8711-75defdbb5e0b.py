import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-39))
r=w0.sketch().segment((-100,-67),(88,-67)).segment((88,-50)).segment((100,-50)).segment((99,67)).segment((89,67)).segment((89,-57)).segment((-100,-57)).close().assemble().push([(90,54)]).circle(7,mode='s').finalize().extrude(78)