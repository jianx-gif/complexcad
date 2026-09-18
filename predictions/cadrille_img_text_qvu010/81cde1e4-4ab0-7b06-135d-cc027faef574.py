import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,25,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(54).circle(16,mode='s').finalize().extrude(-55).union(w1.sketch().arc((-79,17),(11,1),(1,-89)).arc((38,-77),(65,-49)).segment((79,-49)).segment((79,49)).segment((65,49)).arc((0,89),(-65,49)).segment((-79,49)).close().assemble().finalize().extrude(200))