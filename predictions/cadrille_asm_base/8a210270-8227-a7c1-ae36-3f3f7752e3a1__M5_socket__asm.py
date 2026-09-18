import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-17))
w1=cq.Workplane('ZX',origin=(0,-80,0))
r=w0.sketch().segment((-95,57),(-85,47)).segment((-72,60)).segment((-82,70)).close().assemble().push([(80,60)]).circle(13).finalize().extrude(35).union(w0.sketch().push([(-78,-63)]).circle(15).circle(5,mode='s').finalize().extrude(43)).union(w1.sketch().segment((-3,-100),(7,-100)).segment((7,-90)).arc((19,-78),(7,-66)).segment((7,100)).segment((-3,100)).segment((-3,-67)).arc((-17,-78),(-3,-89)).close().assemble().finalize().extrude(160))