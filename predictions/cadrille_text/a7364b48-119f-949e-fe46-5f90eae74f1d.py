import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,0,-100))
r=w0.sketch().segment((-75,2),(-75,4)).segment((-71,4)).segment((-71,10)).arc((-75,5),(-75,2)).assemble().reset().face(w0.sketch().segment((71,-4),(75,-4)).segment((75,-2)).segment((71,-2)).arc((72,-3),(71,-4)).assemble()).finalize().extrude(200)