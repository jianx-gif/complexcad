import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,19,0))
w1=cq.Workplane('ZX',origin=(0,60,0))
r=w0.sketch().push([(11,11)]).circle(89).reset().face(w0.sketch().segment((-27,18),(-23,-2)).segment((67,15)).segment((63,35)).close().assemble(),mode='s').finalize().extrude(-56).union(w1.sketch().arc((17,-52),(45,-49),(70,-35)).segment((70,-34)).arc((89,11),(70,56)).segment((70,57)).arc((49,72),(25,77)).segment((25,80)).segment((17,80)).segment((17,77)).arc((-53,11),(17,-54)).close().assemble().finalize().extrude(4))