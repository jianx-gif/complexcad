import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-12,0))
r=w0.sketch().segment((-30,-17),(30,-17)).segment((30,-1)).segment((12,-1)).segment((12,5)).segment((-12,5)).segment((-12,-1)).segment((-30,-1)).close().assemble().push([(-4,-5)]).circle(6,mode='s').finalize().extrude(200).union(w1.sketch().arc((-1,-100),(17,-83),(16,-58)).arc((11,-81),(-1,-100)).assemble().finalize().extrude(19))