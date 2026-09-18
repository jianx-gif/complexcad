import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-30,-40),(30,-40)).segment((30,40)).segment((-30,40)).segment((-30,10)).segment((-27,10)).arc((26,7),(-26,-5)).segment((-30,-5)).close().assemble().finalize().extrude(-16).union(w0.sketch().segment((-28,-16),(-27,-16)).segment((-27,-17)).arc((-26,-18),(-25,-20)).arc((-24,-21),(-23,-21)).arc((25,20),(-28,-16)).assemble().finalize().extrude(-15))
