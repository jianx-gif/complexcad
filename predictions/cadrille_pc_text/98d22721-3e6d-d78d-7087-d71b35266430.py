import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-100,-68),(93,-68)).segment((93,29)).arc((95,59),(65,61)).segment((-100,61)).close().assemble().push([(-34,-20)]).circle(19,mode='s').finalize().extrude(-26)