import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().arc((-57,-15),(-44,-23),(-36,-38)).arc((44,45),(-57,-15)).assemble().finalize().extrude(-12).union(w0.sketch().push([(17,-52)]).circle(40).circle(12,mode='s').finalize().extrude(99)).union(w0.sketch().push([(17,-52)]).circle(40).circle(33,mode='s').finalize().extrude(130)).union(w1.sketch().arc((-100,2),(99,-12),(-100,4)).segment((-99,4)).segment((-99,2)).close().assemble().finalize().extrude(57))