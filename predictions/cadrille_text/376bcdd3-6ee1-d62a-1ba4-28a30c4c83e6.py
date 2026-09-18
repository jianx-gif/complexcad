import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((35,-52),(40,-57)).segment((43,-57)).arc((35,-49),(27,-58)).assemble().finalize().extrude(80).union(w0.sketch().push([(0,50)]).circle(5).push([(0,49.5)]).rect(6,7,mode='s').finalize().extrude(99)).union(w0.workplane(offset=100/2).moveTo(0,50).cylinder(100,10))