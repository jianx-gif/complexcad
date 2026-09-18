import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,92))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(68).circle(74,mode='s').finalize().extrude(-192).union(w0.sketch().circle(81).circle(68,mode='s').finalize().extrude(-142)).union(w1.sketch().circle(74).circle(68,mode='s').finalize().extrude(-118))