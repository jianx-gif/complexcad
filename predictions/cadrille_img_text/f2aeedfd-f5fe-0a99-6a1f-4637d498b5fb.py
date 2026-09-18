import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,9,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((45,59),(55,44),(59,26)).arc((60,45),(45,59)).assemble().finalize().extrude(-34).union(w1.sketch().arc((-84,-54),(0,-39),(84,-54)).segment((84,-26)).segment((81,-26)).segment((81,-22)).segment((84,-22)).segment((84,26)).segment((-84,26)).close().assemble().finalize().extrude(200))