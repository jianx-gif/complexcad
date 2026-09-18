import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-21))
w1=cq.Workplane('YZ',origin=(-74,0,0))
r=w0.sketch().push([(-49,0)]).rect(102,102).push([(-84,-2)]).circle(4,mode='s').push([(-12,0)]).circle(4,mode='s').finalize().extrude(-14).union(w1.sketch().arc((-1,35),(-5,-1),(11,-33)).segment((11,-18)).arc((2,-12),(11,-6)).segment((11,-3),(1,11)).arc((0,23),(-1,35)).assemble().finalize().extrude(174))