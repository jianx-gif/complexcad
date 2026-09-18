import cadquery as cq
w0=cq.Workplane('XY',origin=(-40,-40,-100))
r=w0.sketch().segment((-39,19),(-39,23)).segment((-35,23)).segment((-35,20)).arc((-37,21),(-39,19)).assemble().finalize().extrude(19).union(w0.sketch().segment((28,-58),(39,-58)).segment((39,-52)).arc((34,-55),(28,-58)).assemble().finalize().extrude(190))