import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,66))
r=w0.sketch().segment((-24,0),(-17,-16)).segment((-12,-14)).arc((5,-23),(19,-9)).segment((24,-7)).segment((17,16)).segment((12,14)).arc((-5,23),(-19,9)).segment((-24,7)).segment((-17,7)).segment((-17,0)).close().assemble().finalize().extrude(-66).union(w0.sketch().circle(35).circle(22,mode='s').finalize().extrude(-6))