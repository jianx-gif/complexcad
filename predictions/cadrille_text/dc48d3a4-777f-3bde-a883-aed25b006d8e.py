import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,0,-100))
r=w0.sketch().segment((26,-58),(50,-58)).segment((50,-48)).close().assemble().finalize().extrude(200)