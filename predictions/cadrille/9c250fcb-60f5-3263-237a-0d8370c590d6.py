import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('YZ',origin=(98,0,0))
r=w0.sketch().segment((20,-10),(46,-10)).segment((46,-14)).segment((53,-14)).segment((48,0)).segment((20,0)).close().assemble().finalize().extrude(-200).union(w1.sketch().arc((-53,-3),(-52,-4),(-50,-5)).segment((20,-5)).segment((20,14)).segment((-50,14)).arc((-52,12),(-53,10)).close().assemble().push([(-16,7)]).circle(5,mode='s').finalize().extrude(-192))