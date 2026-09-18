import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((92,-59),(100,-59)).segment((100,-57)).segment((94,-57)).arc((93,-58),(92,-59)).assemble().finalize().extrude(133).union(w0.sketch().push([(55,-6)]).circle(20).push([(55,-6.5)]).rect(24,17,mode='s').finalize().extrude(133))