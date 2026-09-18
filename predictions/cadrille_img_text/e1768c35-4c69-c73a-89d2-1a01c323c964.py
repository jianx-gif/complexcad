import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-90,0))
w1=cq.Workplane('YZ',origin=(35,0,0))
r=w0.sketch().arc((-100,73),(34,91),(88,-29)).segment((88,-29),(68,-59)).arc((68,-67),(64,-75)).arc((66,-82),(67,-89)).arc((84,-79),(95,-64)).segment((95,-64),(100,-73)).segment((100,73)).segment((95,73)).arc((0,100),(-95,73)).close().assemble().finalize().extrude(179).union(w1.sketch().push([(0,-1)]).circle(59).push([(-43,-10)]).circle(10,mode='s').finalize().extrude(-102))