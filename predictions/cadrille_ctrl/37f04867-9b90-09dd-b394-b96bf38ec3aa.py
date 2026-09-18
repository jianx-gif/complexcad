import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-70/2).moveTo(0,-1).cylinder(70,2).union(w0.sketch().arc((-29,-6),(29,-8),(-26,15)).arc((-30,4),(-29,-6)).assemble().push([(1,1)]).circle(15,mode='s').finalize().extrude(30)).union(w0.sketch().push([(0,-1)]).circle(22).push([(-13,-10)]).circle(2,mode='s').push([(10,0)]).circle(5,mode='s').finalize().extrude(70))
