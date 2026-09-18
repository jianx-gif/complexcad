import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,18))
w1=cq.Workplane('YZ',origin=(-20,0,0))
r=w0.sketch().rect(200,180).reset().face(w0.sketch().segment((-88,-5),(-73,-5)).segment((-73,-54)).segment((73,-54)).segment((73,-5)).segment((88,-5)).segment((88,5)).segment((73,5)).segment((73,54)).segment((-73,54)).segment((-73,5)).segment((-88,5)).close().assemble(),mode='s').finalize().extrude(-18).union(w1.sketch().arc((-40,7),(0,-18),(40,7)).close().assemble().finalize().extrude(-14))