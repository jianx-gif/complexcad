import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-100/2).moveTo(0,-1).cylinder(100,2).union(w0.sketch().arc((-39,10),(39,-10),(-38,13)).segment((-37,13)).segment((-37,10)).close().assemble().circle(38,mode='s').finalize().extrude(100))
