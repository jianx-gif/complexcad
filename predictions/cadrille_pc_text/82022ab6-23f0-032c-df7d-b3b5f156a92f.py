import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,67,0))
r=w0.sketch().circle(34).reset().face(w0.sketch().segment((-21,13),(-15,-21)).segment((21,-13)).segment((15,21)).close().assemble(),mode='s').finalize().extrude(-134).union(w0.sketch().arc((89,-46),(87,-37),(95,-34)).arc((-91,42),(89,-46)).assemble().finalize().extrude(-14))