import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,48))
r=w0.sketch().circle(66).circle(49,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-99,7),(-95,7)).arc((0,-99),(95,7)).segment((99,7)).segment((99,12)).segment((95,12)).arc((0,99),(-95,12)).segment((-99,12)).close().assemble().circle(85,mode='s').finalize().extrude(-53)).union(w1.sketch().circle(94).circle(66,mode='s').finalize().extrude(49))