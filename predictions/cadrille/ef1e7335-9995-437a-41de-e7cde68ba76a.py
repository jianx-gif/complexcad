import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.workplane(offset=14/2).box(200,150,14).union(w0.sketch().segment((-38,-70),(-36,-70)).segment((-36,-75)).segment((36,-75)).segment((36,-70)).segment((38,-70)).segment((38,70)).segment((36,70)).segment((36,75)).segment((-36,75)).segment((-36,70)).segment((-38,70)).close().assemble().circle(13,mode='s').finalize().extrude(44))