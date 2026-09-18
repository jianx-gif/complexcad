import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-89,-48),(-89,48)).arc((-100,0),(-89,-48)).assemble().reset().face(w0.sketch().arc((89,-48),(100,0),(89,48)).close().assemble()).finalize().extrude(-100).union(w0.sketch().push([(0,0.5)]).rect(120,15).push([(0,0)]).circle(5,mode='s').finalize().extrude(-97)).union(w0.sketch().push([(0,1)]).circle(21).circle(17,mode='s').finalize().extrude(39)).union(w1.sketch().arc((-83,50),(0,1),(83,50)).segment((74,50)).arc((0,17),(-74,50)).close().assemble().finalize().extrude(-192))