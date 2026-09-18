import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-40,-24),(40,-24)).segment((40,24)).segment((-39,25)).close().assemble().finalize().extrude(-1).union(w0.sketch().segment((-37,-21),(35,-25)).segment((37,24)).segment((-35,25)).close().assemble().push([(0,1)]).circle(23,mode='s').finalize().extrude(14)).union(w0.sketch().segment((-34,-19),(31,-19)).segment((31,-12)).segment((34,-12)).segment((34,19)).segment((-34,19)).close().assemble().circle(23,mode='s').finalize().extrude(30))
