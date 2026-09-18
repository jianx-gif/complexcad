import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,91))
r=w0.workplane(offset=-191/2).box(28,4,191).union(w0.sketch().segment((-19,6),(-13,-11)).segment((19,-7)).segment((13,11)).close().assemble().circle(3,mode='s').finalize().extrude(-175)).union(w0.sketch().circle(20).circle(15,mode='s').finalize().extrude(9))