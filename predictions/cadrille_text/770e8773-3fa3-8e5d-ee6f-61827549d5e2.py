import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((35,-53),(39,-57)).segment((41,-57)).arc((35,-49),(28,-58)).assemble().finalize().extrude(80).union(w0.sketch().push([(0,50)]).circle(5).push([(0,49.5)]).rect(6,7,mode='s').finalize().extrude(100))