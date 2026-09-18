import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-53,-31),(15,-53),(83,-31)).segment((74,-31)).arc((15,-49),(-43,-31)).close().assemble().finalize().extrude(-68).union(w0.sketch().push([(15,0)]).circle(12).circle(7,mode='s').finalize().extrude(95)).union(w1.sketch().arc((-95,-16),(-88,-18),(-81,-19)).segment((-81,-43)).segment((-63,-43)).segment((-63,-19)).arc((-56,-18),(-49,-16)).close().assemble().finalize().extrude(-200))