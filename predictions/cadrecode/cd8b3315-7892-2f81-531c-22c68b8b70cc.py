import cadquery as cq
w0=cq.Workplane('YZ',origin=(88,0,0))
w1=cq.Workplane('XY',origin=(0,0,17))
r=w0.sketch().segment((-59,-16),(59,-16)).segment((59,12)).segment((49,12)).segment((49,-7)).segment((-49,-7)).segment((-49,12)).segment((-59,12)).close().assemble().finalize().extrude(-188).union(w1.workplane(offset=-24/2).moveTo(94,0).box(12,70,24))