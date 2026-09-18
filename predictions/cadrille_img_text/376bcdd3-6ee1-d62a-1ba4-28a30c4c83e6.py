import cadquery as cq
w0=cq.Workplane('YZ',origin=(-60,0,0))
w1=cq.Workplane('YZ',origin=(-28,0,0))
r=w0.sketch().circle(100).push([(0,3)]).circle(93,mode='s').finalize().extrude(120).union(w1.sketch().arc((-8,-80),(8,0),(-8,80)).close().assemble().finalize().extrude(101))