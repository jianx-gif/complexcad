import cadquery as cq
w0=cq.Workplane('YZ',origin=(-79,0,0))
w1=cq.Workplane('ZX',origin=(0,-20,0))
r=w0.sketch().circle(74).reset().face(w0.sketch().segment((-72,1),(-69,-1)).arc((-58,-38),(-27,-62)).segment((-24,-65)).segment((-22,-63)).arc((38,-58),(69,-7)).segment((72,-1)).segment((69,1)).arc((58,38),(27,62)).segment((24,65)).segment((22,63)).arc((-38,58),(-69,7)).close().assemble(),mode='s').circle(5).finalize().extrude(154).union(w1.sketch().circle(100).circle(91,mode='s').finalize().extrude(25))