import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('ZX',origin=(0,13,0))
r=w0.sketch().segment((-59,46),(-53,39)).arc((-45,-41),(35,-61)).segment((41,-68)).segment((59,-53)).segment((53,-46)).arc((45,41),(-35,61)).segment((-41,68)).close().assemble().finalize().extrude(-79).union(w1.sketch().circle(100).reset().face(w1.sketch().segment((-97,-1),(-61,-1)).arc((0,-61),(61,-1)).segment((97,-1)).segment((97,1)).segment((61,1)).arc((0,61),(-61,1)).segment((-97,1)).close().assemble(),mode='s').finalize().extrude(-23))