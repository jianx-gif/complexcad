import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().segment((-100,-49),(-82,-48)).segment((-74,-5)).segment((-79,-10)).segment((-79,-4)).segment((-71,-4)).segment((-71,-7)).segment((-5,40)).segment((85,-23)).segment((88,-48)).segment((100,-49)).arc((0,48),(-100,-49)).assemble().finalize().extrude(100)