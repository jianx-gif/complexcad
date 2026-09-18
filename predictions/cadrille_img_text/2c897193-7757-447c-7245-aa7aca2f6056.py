import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('XY',origin=(0,0,96))
r=w0.sketch().arc((-100,-92),(59,-61),(95,77)).close().assemble().finalize().extrude(-162).union(w1.sketch().push([(0,17)]).circle(83).circle(54,mode='s').finalize().extrude(-160))