import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-71,0))
w1=cq.Workplane('YZ',origin=(39,0,0))
r=w0.sketch().push([(77,21)]).circle(23).circle(16,mode='s').finalize().extrude(34).union(w0.sketch().arc((-10,59),(59,-51),(1,64)).arc((1,49),(-10,59)).assemble().finalize().extrude(171)).union(w1.sketch().arc((-99,23),(83,-56),(-42,91)).arc((-65,56),(-99,29)).close().assemble().push([(0,5)]).circle(85,mode='s').finalize().extrude(-19))