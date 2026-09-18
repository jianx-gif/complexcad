import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('YZ',origin=(97,0,0))
r=w0.sketch().push([(0,24)]).rect(160,132).circle(67,mode='s').finalize().extrude(5).union(w0.sketch().arc((14,-1),(19,14),(14,29)).close().assemble().finalize().extrude(123)).union(w1.sketch().arc((-85,-58),(0,-89),(85,-58)).segment((85,-57)).arc((70,0),(85,57)).segment((85,58)).arc((0,89),(-85,58)).segment((-85,57)).arc((-70,0),(-85,-57)).close().assemble().push([(-58,-38)]).circle(12,mode='s').push([(0,0)]).rect(64,160,mode='s').push([(-43,78)]).circle(12,mode='s').finalize().extrude(-197))