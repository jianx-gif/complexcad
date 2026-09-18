import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().segment((-5,-1),(5,-1)).segment((5,1)).segment((-5,1)).arc((-4,0),(-5,-1)).assemble().finalize().extrude(-200).union(w1.sketch().segment((27,-58),(36,-58)).segment((36,-51)).arc((32,-54),(27,-58)).assemble().finalize().extrude(-120))