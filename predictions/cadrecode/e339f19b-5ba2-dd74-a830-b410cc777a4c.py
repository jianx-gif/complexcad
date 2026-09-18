import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-37,-22),(-30,-22)).arc((0,-37),(30,-22)).segment((37,-22)).segment((37,22)).segment((30,22)).arc((0,37),(-30,22)).segment((-37,22)).close().assemble().circle(30,mode='s').finalize().extrude(-200).union(w0.sketch().rect(36,20).push([(15,-1)]).circle(3,mode='s').finalize().extrude(-193))