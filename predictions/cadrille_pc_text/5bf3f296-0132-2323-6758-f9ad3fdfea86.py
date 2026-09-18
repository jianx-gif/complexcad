import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,63))
w1=cq.Workplane('XY',origin=(0,0,56))
r=w0.sketch().segment((-100,46),(-93,-53)).segment((100,-46)).segment((93,53)).close().assemble().circle(83,mode='s').finalize().extrude(7).union(w1.sketch().circle(69).circle(35,mode='s').finalize().extrude(-125))