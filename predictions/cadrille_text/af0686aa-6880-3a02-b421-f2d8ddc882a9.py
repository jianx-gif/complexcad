import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,-67,-100))
r=w0.sketch().segment((27,-58),(75,-58)).segment((75,-11)).arc((52,-37),(27,-11)).close().assemble().finalize().extrude(200)