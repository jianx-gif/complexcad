import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,-33,-100))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((33,-55),(36,-57)).segment((39,-57)).arc((33,-52),(27,-58)).assemble().finalize().extrude(200)