import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-10))
w1=cq.Workplane('XY',origin=(-100,-25,-10))
r=w0.sketch().circle(3).circle(2,mode='s').finalize().extrude(110).union(w1.sketch().segment((27,-58),(27,-57)).segment((29,-57)).arc((34,-53),(38,-57)).segment((39,-57)).arc((34,-52),(27,-58)).assemble().finalize().extrude(-80))