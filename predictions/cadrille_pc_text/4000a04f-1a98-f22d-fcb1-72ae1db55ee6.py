import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().circle(100).circle(84,mode='s').finalize().extrude(-126).union(w0.sketch().circle(67).reset().face(w0.sketch().segment((-26,-27),(26,-27)).segment((26,-16)).arc((0,-31),(-26,-16)).close().assemble(),mode='s').reset().face(w0.sketch().arc((-26,16),(0,31),(26,16)).segment((26,27)).segment((-26,27)).close().assemble(),mode='s').finalize().extrude(40)).union(w1.sketch().push([(-30,0)]).circle(50).circle(5,mode='s').finalize().extrude(-89))