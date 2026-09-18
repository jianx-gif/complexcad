import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-8))
w1=cq.Workplane('XY',origin=(-100,-1,-46))
r=w0.sketch().segment((-97,10),(-97,12)).arc((-99,0),(-94,-10)).segment((-94,-8)).segment((-91,-8)).segment((-91,-12)).arc((-80,6),(-97,13)).segment((-94,13)).segment((-94,10)).close().assemble().finalize().extrude(9).union(w1.sketch().segment((65,-42),(65,-38)).arc((64,-36),(65,-34)).segment((65,-30)).arc((61,-36),(65,-42)).assemble().finalize().extrude(92))