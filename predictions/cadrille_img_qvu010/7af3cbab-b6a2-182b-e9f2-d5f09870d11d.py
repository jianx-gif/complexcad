import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-51,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,3)]).circle(58).circle(51,mode='s').finalize().extrude(-11).union(w0.sketch().segment((-92,-16),(-89,-21)).segment((92,16)).segment((89,21)).close().assemble().finalize().extrude(147)).union(w1.sketch().arc((-96,-42),(0,-92),(96,-42)).segment((77,-42)).arc((0,-86),(-77,-42)).close().assemble().reset().face(w1.sketch().segment((-96,42),(-77,42)).arc((0,86),(77,42)).segment((96,42)).arc((0,92),(-96,42)).assemble()).finalize().extrude(-200))