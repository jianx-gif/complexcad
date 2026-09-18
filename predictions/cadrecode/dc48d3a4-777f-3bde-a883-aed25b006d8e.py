import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('XY',origin=(0,0,44))
r=w0.workplane(offset=-143/2).cylinder(143,6).union(w0.sketch().circle(57).circle(45,mode='s').finalize().extrude(-76)).union(w0.sketch().arc((-27,3),(27,-15),(-27,4)).arc((-25,3),(-27,3)).assemble().circle(6,mode='s').finalize().extrude(57)).union(w1.sketch().arc((-68,-8),(68,-8),(-66,18)).segment((-57,18)).segment((-57,-8)).close().assemble().circle(51,mode='s').finalize().extrude(31))