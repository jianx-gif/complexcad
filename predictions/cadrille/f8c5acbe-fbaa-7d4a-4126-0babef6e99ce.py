import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-25))
w1=cq.Workplane('YZ',origin=(-98,0,0))
r=w0.sketch().segment((-100,-50),(100,-50)).segment((100,50)).segment((77,50)).arc((86,44),(93,37)).segment((98,37)).segment((98,-47)).segment((-98,-47)).segment((-98,47)).segment((-75,47)).arc((-76,48),(-77,50)).segment((-100,50)).close().assemble().finalize().extrude(50).union(w1.sketch().rect(76,50).rect(94,46,mode='s').finalize().extrude(196))