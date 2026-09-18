import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((29,-56),(30,-57)).segment((32,-57)).arc((28,-54),(26,-58)).assemble().finalize().extrude(100).union(w0.sketch().push([(0,50)]).circle(5).push([(0,49.5)]).rect(6,7,mode='s').finalize().extrude(100))