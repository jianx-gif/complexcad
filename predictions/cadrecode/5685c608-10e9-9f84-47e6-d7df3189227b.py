import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,77))
r=w0.workplane(offset=-171/2).cylinder(171,62).union(w0.sketch().segment((-68,-1),(-66,-1)).arc((0,-66),(66,-1)).segment((68,-1)).segment((68,1)).segment((66,1)).arc((0,66),(-66,1)).segment((-68,1)).close().assemble().circle(58,mode='s').finalize().extrude(-143)).union(w0.workplane(offset=17/2).cylinder(17,100))