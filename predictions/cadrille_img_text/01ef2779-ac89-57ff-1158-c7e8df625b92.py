import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-89,-83),(53,-83)).segment((89,1)).segment((89,83)).segment((-33,83)).close().assemble().reset().face(w0.sketch().segment((-75,-67),(75,-67)).segment((75,67)).segment((-75,67)).segment((-75,-43)).segment((-75,-44)).close().assemble(),mode='s').finalize().extrude(200)