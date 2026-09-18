import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('XY',origin=(0,0,34))
r=w0.sketch().arc((-100,39),(-81,45),(-61,50)).segment((-100,55)).close().assemble().reset().face(w0.sketch().arc((14,50),(57,42),(96,42)).segment((94,50)).close().assemble()).finalize().extrude(-181).union(w0.sketch().segment((-96,44),(24,61)).arc((-39,74),(-96,44)).assemble().reset().face(w0.sketch().arc((-24,-61),(39,-74),(96,-44)).close().assemble()).finalize().extrude(-109)).union(w1.sketch().push([(40,0)]).rect(68,140).circle(25,mode='s').finalize().extrude(-66))