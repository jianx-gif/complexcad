import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,91))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-83,1),(-69,-45)).segment((-59,-42)).arc((25,-78),(70,4)).segment((83,8)).segment((69,54)).segment((59,51)).arc((-25,77),(-70,4)).close().assemble().push([(0,1)]).circle(69,mode='s').finalize().extrude(-191).union(w1.sketch().push([(0,1)]).circle(80).circle(69,mode='s').finalize().extrude(-162))