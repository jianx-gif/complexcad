import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-47))
r=w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(67).union(w0.sketch().segment((93,-13),(97,-13)).segment((97,14)).segment((93,14)).arc((94,0),(93,-13)).assemble().finalize().extrude(94))