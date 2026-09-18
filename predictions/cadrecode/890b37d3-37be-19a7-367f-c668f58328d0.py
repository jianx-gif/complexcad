import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().rect(200,160).reset().face(w0.sketch().segment((-26,53),(-18,39)).arc((-14,12),(10,2)).segment((18,-12)).segment((26,-8)).segment((18,6)).arc((14,33),(-10,43)).segment((-18,58)).close().assemble(),mode='s').push([(43,46)]).circle(21,mode='s').finalize().extrude(-8)