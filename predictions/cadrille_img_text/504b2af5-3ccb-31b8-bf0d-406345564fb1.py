import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().segment((-89,39),(63,53)).arc((-12,92),(-89,39)).assemble().reset().face(w0.sketch().arc((10,-53),(11,-55),(13,-56)).segment((13,-71)).segment((71,-71)).segment((71,-56)).arc((73,-55),(75,-53)).close().assemble()).finalize().extrude(-200).union(w1.sketch().push([(0,12)]).circle(58).circle(51,mode='s').finalize().extrude(-23))