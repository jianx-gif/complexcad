import cadquery as cq
w0=cq.Workplane('YZ',origin=(71,0,0))
r=w0.sketch().push([(0,-8.5)]).rect(92,69).push([(-29,-3)]).circle(6,mode='s').reset().face(w0.sketch().segment((23,-6),(29,-9)).segment((34,-6)).segment((29,-2)).close().assemble(),mode='s').push([(30,0)]).circle(3,mode='s').finalize().extrude(-171).union(w0.workplane(offset=29/2).moveTo(0,26).box(58,34,29))