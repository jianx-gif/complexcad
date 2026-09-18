import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((35,-52),(39,-57)).segment((42,-57)).arc((35,-50),(27,-58)).assemble().finalize().extrude(100).union(w0.sketch().push([(0,50)]).circle(10).push([(0,50.5)]).rect(16,3,mode='s').finalize().extrude(100))