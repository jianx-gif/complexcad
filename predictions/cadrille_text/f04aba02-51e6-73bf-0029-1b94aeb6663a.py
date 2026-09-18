import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-100,-50))
r=w0.sketch().segment((38,-54),(50,-54)).segment((50,-48)).arc((45,-51),(38,-54)).assemble().finalize().extrude(100).union(w0.sketch().push([(0,100)]).circle(5).push([(0,99.5)]).rect(4,3,mode='s').finalize().extrude(101))