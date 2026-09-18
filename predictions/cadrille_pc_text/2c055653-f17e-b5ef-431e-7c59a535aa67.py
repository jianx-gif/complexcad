import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-16))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-94,-4),(-72,-8)).arc((-69,-37),(-47,-57)).arc((-59,-50),(-68,-39)).segment((7,-99)).segment((94,4)).segment((-7,99)).segment((-49,51)).arc((-50,52),(-50,53)).segment((-72,57)).close().assemble(),mode='s').finalize().extrude(32)