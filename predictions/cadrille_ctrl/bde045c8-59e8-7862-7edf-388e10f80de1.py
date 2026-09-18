import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
w1=cq.Workplane('YZ',origin=(-27,0,0))
r=w0.sketch().push([(-15.5,0)]).rect(111,100).reset().face(w0.sketch().segment((-64,-30),(-40,-30)).segment((-40,-2)).segment((-64,-2)).segment((-64,-15)).arc((-65,-19),(-64,-23)).close().assemble(),mode='s').reset().face(w0.sketch().segment((-56,-29),(-40,-29)).segment((-40,-2)).segment((-56,-2)).segment((-56,-15)).arc((-55,-19),(-56,-23)).close().assemble(),mode='s').push([(-15,0)]).circle(11,mode='s').push([(15.5,0)]).rect(11,62,mode='s').finalize().extrude(6).union(w1.sketch().arc((-10,-4),(-1,-10),(8,-1)).arc((10,0),(11,2)).arc((1,4),(-8,0)).arc((-7,-3),(-10,-4)).assemble().finalize().extrude(-8))
