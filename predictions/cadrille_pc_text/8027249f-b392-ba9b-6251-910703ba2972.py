import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().segment((-87,-46),(87,-46)).segment((87,20)).segment((15,20)).segment((15,19)).segment((13,19)).segment((13,20)).segment((-87,20)).close().assemble().finalize().extrude(-11).union(w0.workplane(offset=13/2).box(14,200,13))