import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-1))
r=w0.sketch().segment((28,-58),(35,-58)).segment((35,-48)).arc((32,-53),(28,-58)).assemble().finalize().extrude(-9).union(w0.sketch().push([(32,-5)]).circle(28).circle(27,mode='s').finalize().extrude(10)).union(w0.sketch().segment((98,-50),(100,-50)).segment((100,-48)).arc((99,-49),(98,-50)).assemble().finalize().extrude(100))