import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-50,35),(-45,-35)).segment((50,-35)).segment((49,-9)).arc((49,-7),(48,-5)).segment((45,35)).segment((1,35)).segment((1,12)).segment((-12,12)).segment((-12,35)).close().assemble().finalize().extrude(-4).union(w0.sketch().push([(0,0.5)]).rect(100,69).push([(0,1)]).circle(17,mode='s').finalize().extrude(1))
