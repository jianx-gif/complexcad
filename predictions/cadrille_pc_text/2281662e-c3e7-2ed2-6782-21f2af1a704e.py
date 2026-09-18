import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-9))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().circle(100).circle(67,mode='s').finalize().extrude(16).union(w1.sketch().segment((-62,-8),(-26,-8)).segment((-26,-40)).segment((26,-40)).segment((26,-8)).segment((62,-8)).segment((62,8)).segment((26,8)).segment((26,40)).segment((-26,40)).segment((-26,8)).segment((-62,8)).close().assemble().finalize().extrude(-26))