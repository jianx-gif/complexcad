import cadquery as cq
w0=cq.Workplane('YZ',origin=(73,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-86,-74),(-67,-83),(-47,-89)).close().assemble().reset().face(w0.sketch().segment((-74,74),(-3,74)).arc((-38,83),(-74,74)).assemble()).reset().face(w0.sketch().arc((47,-89),(67,-83),(86,-74)).close().assemble()).reset().face(w0.sketch().segment((67,67),(86,74)).arc((76,74),(67,72)).close().assemble()).finalize().extrude(-111).union(w1.sketch().segment((-95,-16),(95,-16)).segment((95,-11)).arc((0,-10),(-95,11)).close().assemble().finalize().extrude(-200))