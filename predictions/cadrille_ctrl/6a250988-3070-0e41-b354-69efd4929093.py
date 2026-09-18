import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-25,1),(-23,-15)).segment((-21,-15)).segment((-23,2)).close().assemble().finalize().extrude(35).union(w0.sketch().push([(11,0)]).circle(14).circle(9,mode='s').finalize().extrude(38)).union(w0.sketch().segment((-23,-11),(-22,-15)).segment((19,-18)).segment((20,-11)).segment((1,-9)).arc((-7,-13),(-15,-9)).close().assemble().finalize().extrude(38))
