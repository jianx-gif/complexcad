import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-18,0))
r=w0.sketch().arc((-20,20),(0,29),(20,20)).segment((20,34)).segment((-20,34)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(14,12)]).circle(86).circle(62,mode='s').finalize().extrude(11))