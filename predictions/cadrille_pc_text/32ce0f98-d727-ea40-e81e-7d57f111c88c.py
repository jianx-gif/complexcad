import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(19).circle(15,mode='s').finalize().extrude(-145).union(w1.sketch().arc((-78,78),(-13,1),(36,-78)).arc((13,7),(-78,78)).assemble().finalize().extrude(-33))