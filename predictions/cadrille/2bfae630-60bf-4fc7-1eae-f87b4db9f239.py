import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,92))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(27).reset().face(w0.sketch().segment((-21,-13),(18,-20)).segment((21,13)).segment((-18,20)).close().assemble(),mode='s').finalize().extrude(-192).union(w0.sketch().circle(54).circle(46,mode='s').finalize().extrude(-152)).union(w1.sketch().circle(53).circle(46,mode='s').finalize().extrude(-8))