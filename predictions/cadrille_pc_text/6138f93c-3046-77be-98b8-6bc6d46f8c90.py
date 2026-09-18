import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().circle(44).circle(3,mode='s').finalize().extrude(-191).union(w0.sketch().segment((-52,-38),(52,-38)).segment((52,35)).segment((-47,38)).close().assemble().circle(3,mode='s').finalize().extrude(-39)).union(w0.workplane(offset=9/2).box(104,10,9))