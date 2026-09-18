import cadquery as cq
w0=cq.Workplane('YZ',origin=(15,0,0))
w1=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-32,13),(-20,13)).arc((-26,16),(-32,13)).assemble().reset().face(w0.sketch().arc((-20,4),(-19,8),(-20,12)).close().assemble()).finalize().extrude(-30).union(w0.workplane(offset=-29/2).moveTo(26,11).cylinder(29,5)).union(w0.workplane(offset=65/2).moveTo(0,4).cylinder(65,2)).union(w1.sketch().segment((-30,-20),(30,-20)).segment((30,20)).segment((-30,20)).segment((-30,10)).arc((-29,9),(-30,8)).close().assemble().push([(0,0)]).circle(5,mode='s').finalize().extrude(-8))
