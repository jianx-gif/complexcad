import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
w1=cq.Workplane('ZX',origin=(-30,50,0))
r=w0.sketch().push([(-3.5,0)]).rect(19,200).push([(-3,0)]).circle(8,mode='s').finalize().extrude(-100).union(w1.sketch().arc((13,-30),(14,-27),(16,-24)).arc((-15,27),(13,-26)).close().assemble().finalize().extrude(-67))