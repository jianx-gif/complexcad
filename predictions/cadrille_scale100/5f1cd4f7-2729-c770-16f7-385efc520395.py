import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().segment((0,-22),(24,-18)).segment((24,-15)).arc((12,-18),(0,-15)).close().assemble().finalize().extrude(20).union(w0.sketch().segment((33,16),(80,-4)).segment((80,4)).segment((34,17)).close().assemble().finalize().extrude(20)).union(w0.sketch().push([(12,0)]).circle(21).circle(18,mode='s').finalize().extrude(20))