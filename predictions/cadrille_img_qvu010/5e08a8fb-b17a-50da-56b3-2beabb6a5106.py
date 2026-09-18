import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-56,0))
w1=cq.Workplane('ZX',origin=(0,-61,0))
r=w0.sketch().segment((-85,-68),(85,-68)).segment((85,68)).segment((-85,68)).segment((-85,5)).arc((-82,-1),(-85,-7)).close().assemble().circle(18,mode='s').finalize().extrude(10).union(w0.sketch().segment((-83,-46),(83,-46)).segment((83,46)).segment((82,46)).arc((79,43),(75,46)).segment((-83,46)).close().assemble().finalize().extrude(155)).union(w1.sketch().segment((-100,-66),(-69,-66)).arc((-82,0),(-69,66)).segment((-100,66)).close().assemble().finalize().extrude(-33))