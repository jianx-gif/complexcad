import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().segment((-69,-36),(-69,-35)).arc((0,-75),(69,-35)).segment((69,-36)).arc((81,0),(69,36)).segment((69,35)).arc((0,75),(-69,35)).segment((-69,36)).arc((-81,0),(-69,-36)).assemble().finalize().extrude(-71).union(w0.sketch().arc((-59,-41),(81,51),(-52,-49)).segment((-33,-49)).arc((48,49),(-59,-24)).close().assemble().finalize().extrude(-37)).union(w1.sketch().arc((1,-1),(1,-2),(2,-2)).arc((4,-2),(5,-4)).arc((5,3),(1,-1)).assemble().finalize().extrude(-175))