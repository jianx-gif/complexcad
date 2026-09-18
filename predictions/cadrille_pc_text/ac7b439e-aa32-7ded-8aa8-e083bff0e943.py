import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,39))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(43).circle(42,mode='s').finalize().extrude(32).union(w1.sketch().segment((-32,-19),(-29,-19)).segment((-29,-21)).segment((29,-21)).segment((29,-19)).segment((32,-19)).segment((32,19)).segment((29,19)).segment((29,21)).segment((-29,21)).segment((-29,19)).segment((-32,19)).close().assemble().finalize().extrude(-200))