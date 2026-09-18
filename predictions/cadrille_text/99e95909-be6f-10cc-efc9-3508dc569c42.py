import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-10))
w1=cq.Workplane('XY',origin=(-100,-100,-10))
r=w0.sketch().circle(3).circle(2,mode='s').finalize().extrude(200).union(w1.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((33,-56),(36,-57)).segment((39,-57)).arc((33,-49),(27,-58)).assemble().finalize().extrude(100))