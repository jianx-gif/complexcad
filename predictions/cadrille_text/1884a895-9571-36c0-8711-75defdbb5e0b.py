import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-3))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((33,-56),(36,-57)).segment((39,-57)).arc((33,-54),(27,-58)).assemble().finalize().extrude(-32).union(w0.sketch().face(w0.sketch().segment((99,-15),(99,-13)).segment((100,-13)).arc((96,-17),(100,-15)).close().assemble()).finalize().extrude(39))