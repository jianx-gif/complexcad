import cadquery as cq
w0=cq.Workplane('YZ',origin=(67,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-35,12),(-32,-16)).segment((-15,-14)).segment((-19,20)).arc((-26,17),(-35,12)).assemble().finalize().extrude(-135).union(w1.sketch().rect(150,12).push([(-27,1)]).circle(5,mode='s').finalize().extrude(-200))