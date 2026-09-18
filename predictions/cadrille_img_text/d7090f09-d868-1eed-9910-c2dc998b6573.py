import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-43,0))
w1=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().segment((-68,66),(-66,64)).arc((-65,-49),(44,-78)).segment((46,-80)).segment((50,-76)).arc((69,-65),(85,-50)).segment((89,-46)).segment((88,-44)).arc((87,49),(0,88)).segment((-2,90)).segment((-6,86)).arc((-25,76),(-42,62)).close().assemble().push([(13,6)]).circle(85,mode='s').finalize().extrude(83).union(w1.sketch().arc((10,-73),(29,-76),(48,-73)).close().assemble().finalize().extrude(-148))