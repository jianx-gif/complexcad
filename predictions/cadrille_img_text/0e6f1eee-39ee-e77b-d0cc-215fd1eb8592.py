import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('XY',origin=(0,0,96))
r=w0.sketch().push([(0,13)]).rect(180,174).push([(0,12)]).circle(87,mode='s').circle(12).finalize().extrude(138).union(w1.sketch().arc((-19,-59),(0,-60),(19,-59)).close().assemble().finalize().extrude(-161))