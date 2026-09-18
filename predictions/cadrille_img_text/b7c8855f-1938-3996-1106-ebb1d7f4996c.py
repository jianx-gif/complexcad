import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,93))
w1=cq.Workplane('ZX',origin=(0,-26,0))
r=w0.sketch().arc((-61,-39),(1,-31),(61,-48)).arc((68,-39),(73,-30)).segment((67,-30)).segment((67,30)).segment((73,30)).arc((68,39),(61,48)).arc((1,31),(-61,48)).arc((-54,39),(-48,30)).segment((-42,30)).segment((-42,-30)).segment((-48,-30)).arc((-54,-39),(-61,-39)).assemble().finalize().extrude(-117).union(w1.sketch().push([(-1.5,0)]).rect(197,200).push([(1,0)]).circle(89,mode='s').finalize().extrude(43))