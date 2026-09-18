import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,96,0))
r=w0.sketch().arc((-18,-78),(35,-66),(80,-33)).segment((80,33)).arc((35,66),(-18,78)).segment((-18,33)).arc((32,0),(-18,-33)).close().assemble().finalize().extrude(-196).union(w1.sketch().circle(91).circle(86,mode='s').finalize().extrude(-196))