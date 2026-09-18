import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-50),(75,-50)).segment((75,50)).segment((-75,50)).segment((-75,48)).segment((-70,48)).segment((-70,-48)).segment((-75,-48)).close().assemble().finalize().extrude(-200).union(w0.sketch().circle(36).circle(29,mode='s').finalize().extrude(-195))