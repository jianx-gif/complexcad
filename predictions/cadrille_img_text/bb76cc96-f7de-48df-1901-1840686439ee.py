import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-33,0))
r=w0.sketch().segment((-35,-55),(70,-55)).segment((70,-22)).arc((12,15),(-35,67)).close().assemble().finalize().extrude(181).union(w0.sketch().segment((-70,-67),(-70,-66)).segment((35,-66)).arc((-18,100),(-70,-67)).assemble().finalize().extrude(200)).union(w1.sketch().push([(-68,26)]).circle(62).push([(-68,26.5)]).rect(48,13,mode='s').finalize().extrude(69))