import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((78,-26),(78,-16),(82,-7)).arc((-79,16),(78,-26)).assemble().finalize().extrude(-200)