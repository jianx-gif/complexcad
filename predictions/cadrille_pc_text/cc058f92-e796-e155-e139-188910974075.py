import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-100,-87),(100,-87)).segment((100,-72)).segment((45,-72)).segment((45,-82)).segment((-40,-82)).segment((-40,-72)).segment((-85,-72)).segment((-85,87)).segment((-100,87)).close().assemble().push([(-92,0)]).circle(7,mode='s').finalize().extrude(-30)