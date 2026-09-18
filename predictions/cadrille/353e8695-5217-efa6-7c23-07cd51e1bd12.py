import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-67))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,-1),(-83,-2)).arc((-60,-57),(-6,-83)).segment((-5,-84)).segment((-4,-83)).arc((57,-53),(83,7)).segment((84,8)).segment((83,9)).arc((60,64),(6,83)).segment((5,84)).segment((4,83)).arc((-57,53),(-83,-1)).close().assemble(),mode='s').finalize().extrude(134)