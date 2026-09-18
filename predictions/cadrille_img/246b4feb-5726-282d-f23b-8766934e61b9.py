import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,59,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,19)]).circle(29).circle(22,mode='s').finalize().extrude(-139).union(w0.sketch().push([(0,19)]).circle(19).circle(15,mode='s').finalize().extrude(-11)).union(w1.sketch().arc((-79,1),(-78,-1),(-78,-3)).arc((-1,-79),(96,-29)).arc((96,-27),(97,-25)).arc((98,-10),(97,4)).arc((96,6),(96,8)).arc((1,79),(-79,1)).assemble().push([(1,0)]).circle(78,mode='s').finalize().extrude(-172))