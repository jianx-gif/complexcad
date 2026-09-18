import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-70,11),(0,-11),(70,11)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-70,17),(0,-78),(70,17)).segment((69,17)).arc((0,-75),(-69,17)).close().assemble().finalize().extrude(-181))