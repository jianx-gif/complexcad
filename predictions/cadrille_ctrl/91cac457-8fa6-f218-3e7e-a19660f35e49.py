import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
w1=cq.Workplane('XY',origin=(0,0,-4))
r=w0.sketch().segment((-45,-1),(-39,-5)).arc((-24,-32),(5,-40)).segment((11,-44)).segment((16,-36)).arc((32,-24),(39,-5)).segment((45,1)).segment((39,5)).arc((24,32),(-5,40)).segment((-11,44)).segment((-16,36)).arc((-32,24),(-39,5)).close().assemble().circle(20,mode='s').finalize().extrude(-8).union(w0.sketch().arc((-38,13),(36,-16),(-37,15)).segment((-37,13)).close().assemble().finalize().extrude(-8)).union(w1.sketch().arc((-1,-45),(4,-41),(8,-37)).segment((-1,-37)).close().assemble().finalize().extrude(11))
