import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-55,24),(-20,-15),(30,-24)).segment((30,-58)).arc((12,10),(-55,24)).assemble().finalize().extrude(-200)