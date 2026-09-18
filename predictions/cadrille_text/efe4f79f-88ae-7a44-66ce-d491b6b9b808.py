import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,15,-1))
r=w0.sketch().segment((64,-52),(64,-49)).arc((59,-50),(64,-52)).assemble().finalize().extrude(-18).union(w0.sketch().push([(5,0)]).circle(3).circle(2,mode='s').finalize().extrude(15))