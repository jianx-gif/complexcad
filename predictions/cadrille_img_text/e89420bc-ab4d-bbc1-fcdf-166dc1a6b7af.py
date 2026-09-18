import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-3,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-96,92),(-80,-29)).arc((-45,33),(23,58)).segment((23,65)).segment((39,65)).arc((74,49),(100,21)).segment((84,96)).arc((11,86),(-55,92)).close().assemble().finalize().extrude(-10).union(w0.sketch().push([(0,1)]).circle(59).push([(25,26)]).circle(20,mode='s').finalize().extrude(83)).union(w1.sketch().arc((-91,-29),(0,-65),(91,-29)).close().assemble().finalize().extrude(200))