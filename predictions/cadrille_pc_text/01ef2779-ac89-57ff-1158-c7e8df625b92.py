import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-50,-37),(50,-38)).segment((50,37)).segment((-50,38)).close().assemble().rect(74,50,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-48,19),(-47,19)).segment((-47,17)).arc((-42,24),(-48,19)).assemble().finalize().extrude(-34))