import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-73,0,0))
r=w0.sketch().segment((-98,-23),(-65,-23)).segment((-65,-19)).segment((-63,-19)).segment((-63,-23)).segment((29,19)).segment((98,-19)).segment((-84,55)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-98,-29),(-48,73),(50,100)).arc((-44,75),(-98,-29)).assemble().push([(-1,72)]).circle(5,mode='s').finalize().extrude(149))