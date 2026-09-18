import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-100,-90),(-95,-90)).segment((-95,-94)).segment((95,-94)).segment((95,-90)).segment((100,-90)).segment((100,94)).segment((95,94)).segment((95,97)).segment((-95,97)).segment((-95,94)).segment((-100,94)).close().assemble().finalize().extrude(-200).union(w0.workplane(offset=-191/2).box(180,200,191))