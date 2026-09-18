import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
w1=cq.Workplane('YZ',origin=(40,0,0))
r=w0.sketch().segment((-35,-10),(-27,-10)).segment((-27,10)).segment((-35,10)).segment((-35,8)).arc((-33,7),(-35,6)).close().assemble().finalize().extrude(-14).union(w1.sketch().push([(0,5)]).rect(100,10).push([(-26,7)]).circle(4,mode='s').push([(0,5)]).circle(4,mode='s').finalize().extrude(-111))