import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-14))
w1=cq.Workplane('XY',origin=(0,0,-62))
r=w0.sketch().circle(86).reset().face(w0.sketch().segment((-50,28),(-34,-33)).segment((-28,-31)).arc((16,-35),(49,-3)).segment((50,-2)).segment((49,-1)).arc((49,3),(48,7)).segment((43,33)).segment((34,31)).arc((-10,39),(-43,3)).close().assemble(),mode='s').finalize().extrude(-86).union(w1.sketch().arc((-62,-19),(-32,-18),(-52,-41)).arc((58,23),(-62,-19)).assemble().push([(22,3)]).circle(24,mode='s').finalize().extrude(162))