import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('ZX',origin=(0,71,0))
r=w0.sketch().segment((-42,-16),(-27,-16)).arc((0,-31),(27,-16)).segment((42,-16)).segment((42,16)).segment((27,16)).arc((0,31),(-27,16)).segment((-42,16)).close().assemble().circle(25,mode='s').finalize().extrude(-46).union(w1.sketch().arc((-55,86),(51,-86),(-49,89)).arc((-49,82),(-55,86)).assemble().circle(86,mode='s').finalize().extrude(-141))