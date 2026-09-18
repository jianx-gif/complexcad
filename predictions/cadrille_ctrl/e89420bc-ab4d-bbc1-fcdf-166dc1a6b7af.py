import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-40,-19),(-32,-20)).arc((-36,-17),(-39,-14)).close().assemble().finalize().extrude(-10).union(w0.sketch().segment((-36,15),(-32,-1)).segment((40,-19)).segment((40,-15)).segment((28,-15)).segment((28,-10)).segment((40,-10)).segment((40,-1)).segment((41,-1)).segment((39,19)).close().assemble().finalize().extrude(-5)).union(w0.sketch().push([(4,0)]).circle(30).push([(25,-10)]).circle(4,mode='s').finalize().extrude(-5))
