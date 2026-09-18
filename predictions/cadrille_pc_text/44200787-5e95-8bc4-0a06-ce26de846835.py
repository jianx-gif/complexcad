import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-64,0))
r=w0.sketch().segment((-11,-100),(4,-100)).segment((4,9)).segment((11,9)).segment((11,100)).segment((-11,100)).close().assemble().finalize().extrude(37).union(w0.sketch().segment((-9,-49),(-6,-49)).segment((-6,-41)).segment((-9,-41)).segment((-9,-43)).arc((-7,-44),(-9,-45)).close().assemble().finalize().extrude(128))