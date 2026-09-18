import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-33,-33))
r=w0.sketch().segment((96,-33),(100,-33)).segment((100,-27)).arc((98,-30),(96,-33)).assemble().finalize().extrude(67).union(w0.sketch().push([(100,-31)]).circle(3).push([(99.5,-31)]).rect(3,4,mode='s').finalize().extrude(67))