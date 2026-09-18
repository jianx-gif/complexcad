import cadquery as cq
w0=cq.Workplane('XY',origin=(-70,0,-100))
r=w0.sketch().segment((-70,77),(-69,77)).segment((-69,79)).close().assemble().reset().face(w0.sketch().segment((24,-58),(70,-2)).segment((24,-2)).close().assemble()).reset().face(w0.sketch().segment((69,-79),(70,-77)).segment((69,-77)).close().assemble()).finalize().extrude(200)