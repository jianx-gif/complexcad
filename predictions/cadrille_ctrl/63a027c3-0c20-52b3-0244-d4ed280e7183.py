import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,14))
r=w0.sketch().segment((27,28),(27,36)).arc((-45,-5),(36,-27)).segment((28,-27)).segment((28,-21)).segment((39,-21)).arc((44,7),(29,32)).segment((29,28)).close().assemble().push([(-28,-30)]).circle(2,mode='s').finalize().extrude(-14).union(w0.sketch().segment((-21,1),(-19,1)).arc((0,-21),(19,1)).segment((21,1)).segment((21,4)).segment((19,4)).arc((0,21),(-19,4)).segment((-21,4)).close().assemble().rect(10,2,mode='s').finalize().extrude(6))
