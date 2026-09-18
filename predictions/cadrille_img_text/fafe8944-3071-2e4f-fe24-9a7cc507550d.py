import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-79,-67),(79,-67)).segment((79,67)).segment((-79,67)).segment((-79,65)).segment((-77,65)).segment((-77,63)).segment((-79,63)).close().assemble().finalize().extrude(120).union(w1.sketch().arc((-46,-89),(0,-77),(46,-89)).segment((46,-77)).arc((0,-86),(-46,-77)).close().assemble().finalize().extrude(200))