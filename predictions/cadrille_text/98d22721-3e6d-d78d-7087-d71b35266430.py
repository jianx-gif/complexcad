import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-36,-36))
r=w0.sketch().segment((69,-52),(100,-52)).segment((100,-48)).segment((71,-48)).arc((71,-50),(69,-52)).assemble().finalize().extrude(72).union(w0.workplane(offset=72/2).moveTo(0,1).cylinder(72,7))