import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-53,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-48,29),(-44,27),(-40,25)).segment((-40,48)).arc((-44,39),(-48,29)).assemble().finalize().extrude(48).union(w0.sketch().arc((84,-48),(94,-37),(100,-24)).segment((84,-24)).close().assemble().finalize().extrude(149)).union(w1.sketch().arc((-59,-58),(12,-55),(82,-66)).segment((82,-26)).arc((15,12),(-59,-26)).close().assemble().finalize().extrude(200))