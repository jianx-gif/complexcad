import cadquery as cq
w0=cq.Workplane('YZ',origin=(-88,0,0))
w1=cq.Workplane('YZ',origin=(-33,0,0))
r=w0.sketch().arc((-58,-46),(0,-71),(58,-46)).segment((57,-46)).arc((0,-70),(-57,-46)).close().assemble().reset().face(w0.sketch().segment((-58,46),(-57,46)).arc((0,70),(57,46)).segment((58,46)).arc((0,71),(-58,46)).assemble()).finalize().extrude(188).union(w1.sketch().circle(100).push([(0,1)]).circle(99,mode='s').finalize().extrude(100))