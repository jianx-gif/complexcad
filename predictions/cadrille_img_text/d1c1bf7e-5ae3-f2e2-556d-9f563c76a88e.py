import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('YZ',origin=(-58,0,0))
r=w0.sketch().arc((-39,-26),(11,-29),(49,-5)).arc((50,-3),(52,-2)).arc((58,3),(64,7)).arc((67,10),(70,13)).arc((24,39),(-10,80)).arc((-31,30),(-39,-26)).assemble().finalize().extrude(-178).union(w1.sketch().push([(0,-1)]).circle(99).circle(87,mode='s').finalize().extrude(-22))