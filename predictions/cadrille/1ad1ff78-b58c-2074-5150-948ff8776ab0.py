import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-21))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().rect(110,190).reset().face(w0.sketch().segment((-55,-78),(-29,-78)).segment((-29,-94)).segment((29,-94)).segment((29,-78)).segment((55,-78)).segment((55,78)).segment((29,78)).segment((29,94)).segment((-29,94)).segment((-29,78)).segment((-55,78)).close().assemble(),mode='s').finalize().extrude(-8).union(w1.sketch().push([(0,3.5)]).rect(124,49).rect(114,41,mode='s').finalize().extrude(200))