import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('XY',origin=(0,0,-25))
r=w0.sketch().segment((-50,-4),(50,-4)).segment((50,11)).segment((38,11)).segment((38,0)).segment((26,0)).segment((26,11)).segment((-50,11)).close().assemble().push([(-22.5,5)]).rect(31,8,mode='s').finalize().extrude(200).union(w1.sketch().push([(-75,0)]).circle(18).circle(16,mode='s').finalize().extrude(50))