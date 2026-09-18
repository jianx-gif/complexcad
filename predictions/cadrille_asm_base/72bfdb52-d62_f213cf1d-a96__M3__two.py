import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
w1=cq.Workplane('YZ',origin=(31,0,0))
r=w0.sketch().segment((-35,-66),(76,-66)).segment((76,6)).arc((35,98),(-35,26)).close().assemble().reset().face(w0.sketch().segment((-26,-55),(67,-55)).segment((67,-1)).arc((21,-22),(-26,-1)).close().assemble(),mode='s').finalize().extrude(7).union(w1.sketch().segment((-100,0),(-19,0)).segment((-19,8)).segment((-38,8)).arc((-68,9),(-96,8)).segment((-100,0)).assemble().finalize().extrude(-107))