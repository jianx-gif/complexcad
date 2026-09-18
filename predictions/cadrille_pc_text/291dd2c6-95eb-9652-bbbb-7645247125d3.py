import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((59,54),(59,67)).segment((74,67)).arc((73,69),(73,71)).arc((75,66),(78,61)).segment((78,58)).segment((80,58)).segment((80,54)).segment((78,54)).segment((78,51)).segment((74,51)).segment((74,54)).close().assemble().finalize().extrude(-25).union(w0.sketch().circle(100).circle(65,mode='s').finalize().extrude(-24))