import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-70))
r=w0.sketch().circle(99).circle(51,mode='s').finalize().extrude(-5).union(w0.sketch().segment((-92,41),(-84,37)).arc((-5,-99),(90,29)).segment((92,31)).segment((89,33)).arc((25,97),(-63,77)).segment((-66,79)).close().assemble().circle(95,mode='s').circle(35).finalize().extrude(145))