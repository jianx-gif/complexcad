import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('YZ',origin=(79,0,0))
r=w0.sketch().arc((54,-39),(66,-23),(78,-7)).segment((54,-7)).close().assemble().reset().face(w0.sketch().segment((54,39),(78,39)).arc((66,55),(54,69)).close().assemble()).finalize().extrude(128).union(w1.sketch().segment((-19,-100),(19,-100)).segment((19,-95)).arc((97,0),(19,95)).segment((19,100)).segment((-19,100)).segment((-19,95)).arc((-97,0),(-19,-95)).close().assemble().circle(91,mode='s').finalize().extrude(-137))