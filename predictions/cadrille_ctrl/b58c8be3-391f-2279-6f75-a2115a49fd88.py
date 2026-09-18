import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,31))
r=w0.workplane(offset=-101/2).moveTo(0,-1).cylinder(101,2).union(w0.sketch().arc((-28,-11),(-26,-15),(-23,-19)).segment((-23,-18)).arc((-26,-14),(-28,-10)).close().assemble().reset().face(w0.sketch().arc((-28,-7),(-26,-3),(-23,0)).segment((-23,19)).arc((-29,5),(-28,-7)).assemble()).reset().face(w0.sketch().arc((-19,-23),(29,-8),(0,30)).segment((0,29)).arc((28,-7),(-13,-18)).segment((-13,-23)).close().assemble()).finalize().extrude(31)).union(w0.workplane(offset=39/2).moveTo(0,-1).cylinder(39,14))
