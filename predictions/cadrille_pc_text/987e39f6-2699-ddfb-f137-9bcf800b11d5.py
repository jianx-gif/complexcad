import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-8,-1))
r=w0.sketch().circle(100).rect(176,14,mode='s').push([(41,-74)]).circle(8,mode='s').finalize().extrude(13).union(w0.sketch().segment((-82,7),(-7,7)).segment((-7,1)).segment((7,1)).segment((7,7)).segment((82,7)).arc((0,82),(-82,7)).assemble().finalize().extrude(14))