import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('YZ',origin=(37,0,0))
r=w0.sketch().segment((-2,-14),(0,-14)).segment((0,-16)).arc((2,16),(-2,-14)).assemble().finalize().extrude(-198).union(w0.sketch().circle(49).circle(5,mode='s').finalize().extrude(-143)).union(w0.sketch().segment((-99,-14),(-85,-14)).segment((-85,-49)).arc((98,19),(-99,-14)).assemble().finalize().extrude(-5)).union(w1.sketch().push([(28,0)]).circle(67).circle(63,mode='s').finalize().extrude(-98))