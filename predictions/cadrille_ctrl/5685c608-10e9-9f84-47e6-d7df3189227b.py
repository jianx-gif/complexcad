import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,66))
r=w0.sketch().segment((-24,0),(-17,-16)).segment((-13,-14)).arc((7,-22),(20,-4)).segment((24,-2)).segment((17,14)).segment((13,14)).arc((-7,22),(-20,4)).close().assemble().finalize().extrude(-66).union(w0.sketch().circle(35).circle(19,mode='s').finalize().extrude(-6))
