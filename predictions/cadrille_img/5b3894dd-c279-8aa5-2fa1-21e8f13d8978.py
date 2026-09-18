import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('YZ',origin=(29,0,0))
r=w0.sketch().segment((-51,-68),(-49,-68)).arc((24,-94),(96,-68)).segment((98,-68)).segment((98,-65)).arc((100,-60),(100,-55)).arc((97,-57),(94,-59)).arc((93,-62),(91,-64)).segment((91,-65)).segment((89,-65)).arc((87,-66),(86,-68)).segment((94,-68)).arc((24,-93),(-46,-68)).close().assemble().finalize().extrude(194).union(w1.sketch().push([(0,14)]).circle(86).circle(80,mode='s').finalize().extrude(-123))