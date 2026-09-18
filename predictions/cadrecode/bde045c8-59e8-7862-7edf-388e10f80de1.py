import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-18/2).moveTo(-29,0).cylinder(18,18).union(w0.sketch().rect(200,180).reset().face(w0.sketch().segment((-73,-54),(17,-54)).segment((17,7)).segment((44,7)).segment((44,-54)).segment((73,-54)).segment((73,54)).segment((-73,54)).close().assemble(),mode='s').finalize().extrude(18))