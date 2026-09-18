import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-71))
w1=cq.Workplane('ZX',origin=(0,59,0))
r=w0.sketch().arc((10,-93),(75,-63),(84,7)).arc((-64,57),(10,-93)).assemble().finalize().extrude(134).union(w0.sketch().arc((-50,11),(-36,-29),(-4,-56)).segment((-4,-58)).segment((-1,-58)).arc((39,-58),(74,-39)).segment((77,-39)).segment((77,-37)).arc((91,-1),(81,36)).arc((22,-38),(-50,11)).assemble().finalize().extrude(171)).union(w1.sketch().arc((-100,4),(-96,1),(-92,-2)).arc((39,38),(-10,-80)).arc((-8,-84),(-6,-88)).arc((44,47),(-100,4)).assemble().finalize().extrude(14))