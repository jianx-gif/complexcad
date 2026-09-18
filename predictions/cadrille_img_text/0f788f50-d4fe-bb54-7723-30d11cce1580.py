import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('YZ',origin=(98,0,0))
r=w0.sketch().segment((-100,-98),(100,-98)).segment((100,98)).segment((-100,98)).segment((-100,86)).segment((-97,86)).segment((-97,82)).segment((-100,82)).close().assemble().circle(97,mode='s').finalize().extrude(-29).union(w0.sketch().arc((12,-1),(17,1),(18,6)).arc((16,3),(12,1)).close().assemble().finalize().extrude(115)).union(w1.sketch().arc((-38,-32),(-36,-31),(-33,-31)).segment((-33,100)).segment((-38,100)).close().assemble().finalize().extrude(-146))