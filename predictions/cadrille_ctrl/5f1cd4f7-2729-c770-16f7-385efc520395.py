import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().segment((0,-22),(23,-18)).segment((22,-14)).arc((11,-18),(0,-17)).close().assemble().finalize().extrude(20).union(w0.sketch().segment((33,16),(80,-4)).segment((80,4)).segment((34,18)).close().assemble().finalize().extrude(20)).union(w0.sketch().push([(44,0)]).circle(14).circle(13,mode='s').finalize().extrude(20))
