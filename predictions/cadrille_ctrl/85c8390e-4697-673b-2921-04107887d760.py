import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().arc((11,-44),(16,-41),(21,-40)).arc((22,-39),(23,-38)).segment((20,-38)).arc((25,-36),(30,-36)).arc((-22,39),(11,-44)).assemble().push([(43,2)]).circle(2,mode='s').finalize().extrude(-30).union(w0.workplane(offset=-30/2).moveTo(0,-1).cylinder(30,44))
