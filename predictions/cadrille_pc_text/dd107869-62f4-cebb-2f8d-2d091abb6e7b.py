import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('YZ',origin=(-73,0,0))
r=w0.sketch().arc((-4,-8),(4,-7),(-4,-6)).arc((-2,-7),(-4,-8)).assemble().finalize().extrude(200).union(w1.sketch().push([(-47.5,7.5)]).rect(21,15).push([(-47,7)]).circle(4,mode='s').finalize().extrude(55))