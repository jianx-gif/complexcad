import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('ZX',origin=(0,-95,0))
r=w0.sketch().circle(100).circle(26,mode='s').finalize().extrude(-28).union(w0.sketch().segment((-70,45),(-37,45)).segment((-37,44)).segment((37,44)).segment((37,45)).segment((70,45)).arc((0,75),(-70,45)).assemble().finalize().extrude(39)).union(w1.workplane(offset=190/2).cylinder(190,2))