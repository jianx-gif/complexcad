import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((26,-58),(26,-57)).arc((24,-54),(26,-51)).segment((26,-50)).segment((28,-50)).segment((28,-51)).arc((30,-54),(28,-57)).segment((28,-58)).arc((63,-50),(26,-58)).assemble().finalize().extrude(99).union(w0.sketch().push([(0,50)]).rect(200,6).push([(0,50.5)]).rect(4,5,mode='s').finalize().extrude(100))