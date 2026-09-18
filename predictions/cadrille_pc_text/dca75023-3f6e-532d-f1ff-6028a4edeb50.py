import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,67,0))
r=w0.sketch().rect(40,200).reset().face(w0.sketch().segment((-20,-24),(-12,-27)).segment((-10,-23)).segment((-18,-20)).close().assemble(),mode='s').circle(2,mode='s').push([(16,-88)]).circle(5,mode='s').finalize().extrude(-134)