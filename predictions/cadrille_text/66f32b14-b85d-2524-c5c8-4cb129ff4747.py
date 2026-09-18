import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-1))
w1=cq.Workplane('XY',origin=(-100,0,-46))
r=w0.sketch().segment((-100,91),(-99,91)).segment((-99,92)).close().assemble().finalize().extrude(101).union(w1.sketch().segment((65,-42),(65,-39)).segment((68,-39)).arc((69,-37),(70,-39)).segment((73,-39)).arc((69,-36),(65,-42)).assemble().finalize().extrude(-16))