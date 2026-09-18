import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,-34))
r=w0.sketch().rect(100,180).circle(75,mode='s').finalize().extrude(-183).union(w0.sketch().arc((-99,-22),(98,21),(-98,-26)).segment((-89,-26)).arc((-87,-28),(-84,-29)).segment((-84,-34)).segment((-79,-34)).arc((-80,-32),(-82,-29)).arc((-85,-27),(-88,-24)).segment((-88,-22)).close().assemble().finalize().extrude(-183)).union(w1.sketch().push([(0,34)]).circle(66).circle(53,mode='s').finalize().extrude(134))