import cadquery as cq
w0=cq.Workplane('XY',origin=(-58,0,-57))
r=w0.sketch().segment((97,-49),(97,-47)).segment((99,-47)).arc((93,-42),(97,-49)).assemble().finalize().extrude(-33).union(w0.sketch().push([(52,-1)]).circle(2).push([(52,-0.5)]).rect(2,3,mode='s').finalize().extrude(110)).union(w0.workplane(offset=117/2).moveTo(52,-1).cylinder(117,2))