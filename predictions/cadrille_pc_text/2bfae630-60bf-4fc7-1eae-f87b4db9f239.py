import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,92))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(27).circle(19,mode='s').finalize().extrude(-192).union(w1.sketch().circle(54).circle(46,mode='s').finalize().extrude(-160))