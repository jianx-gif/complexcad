import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((92,-1),(98,-1)).segment((98,1)).segment((92,1)).arc((93,0),(92,-1)).assemble(),mode='s').finalize().extrude(66)