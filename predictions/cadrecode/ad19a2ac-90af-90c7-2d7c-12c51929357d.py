import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-59))
r=w0.sketch().circle(100).reset().face(w0.sketch().arc((56,36),(-62,-25),(66,10)).arc((65,15),(63,20)).segment((93,14)).segment((95,21)).segment((60,28)).arc((58,32),(56,36)).assemble(),mode='s').finalize().extrude(118)