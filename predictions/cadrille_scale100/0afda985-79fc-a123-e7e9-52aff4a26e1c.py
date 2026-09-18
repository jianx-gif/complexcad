import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
w1=cq.Workplane('XY',origin=(0,0,80))
r=w0.workplane(offset=-90/2).moveTo(0,-4).box(12,8,90).union(w0.sketch().circle(10).circle(4,mode='s').finalize().extrude(-39)).union(w1.sketch().segment((-6,-8),(6,-8)).segment((6,4)).arc((0,0),(-6,1)).close().assemble().finalize().extrude(-140))