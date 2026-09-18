import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-65,0))
r=w0.sketch().push([(0,22)]).circle(68).circle(24,mode='s').finalize().extrude(17).union(w0.sketch().arc((-24,-89),(-1,-66),(1,-34)).close().assemble().finalize().extrude(196)).union(w1.sketch().arc((-45,-33),(1,-21),(35,11)).arc((49,19),(58,32)).arc((61,34),(63,36)).arc((37,55),(31,85)).arc((1,68),(-10,35)).arc((-27,10),(-27,-20)).arc((-36,-26),(-45,-33)).assemble().finalize().extrude(165))