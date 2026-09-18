import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(64,22)]).circle(11).circle(7,mode='s').finalize().extrude(12).union(w0.sketch().segment((-29,52),(29,52)).arc((0,57),(-29,52)).assemble().finalize().extrude(121)).union(w1.sketch().arc((-99,-52),(0,-81),(99,-52)).segment((91,-52)).segment((91,-38)).arc((89,-29),(91,-20)).segment((91,20)).arc((89,29),(91,38)).segment((91,52)).segment((-91,52)).segment((-91,-52)).close().assemble().finalize().extrude(-200))