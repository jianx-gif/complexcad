import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().circle(100).circle(72,mode='s').circle(41).push([(78,-15)]).circle(20,mode='s').finalize().extrude(-10).union(w0.sketch().arc((-65,57),(-63,59),(-60,61)).arc((49,71),(65,-37)).arc((63,-49),(59,-61)).arc((49,79),(-65,57)).assemble().finalize().extrude(85)).union(w1.sketch().circle(91).push([(-1,-31)]).circle(19,mode='s').finalize().extrude(-19))