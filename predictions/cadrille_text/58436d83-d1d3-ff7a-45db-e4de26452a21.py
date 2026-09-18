import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,16,0))
w1=cq.Workplane('ZX',origin=(-5,16,0))
r=w0.sketch().face(w0.sketch().segment((-5,53),(5,53)).arc((0,54),(-5,53)).assemble()).finalize().extrude(-32).union(w1.sketch().face(w1.sketch().arc((35,-47),(37,-46),(39,-46)).segment((39,-44)).segment((41,-44)).segment((41,-46)).arc((43,-46),(45,-47)).arc((43,-45),(41,-44)).segment((41,-42)).segment((39,-42)).segment((39,-44)).arc((36,-45),(35,-47)).assemble()).finalize().extrude(-36))