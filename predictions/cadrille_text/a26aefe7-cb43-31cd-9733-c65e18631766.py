import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-67,78),(-66,78)).segment((-66,80)).close().assemble().reset().face(w0.sketch().segment((66,-80),(67,-78)).segment((66,-78)).close().assemble()).finalize().extrude(-200)