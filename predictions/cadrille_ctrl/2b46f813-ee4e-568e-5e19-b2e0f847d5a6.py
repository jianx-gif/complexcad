import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
w1=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((38,-6),(41,-6)).segment((41,0)).arc((80,37),(41,75)).segment((41,80)).segment((38,80)).segment((38,75)).arc((0,37),(38,0)).close().assemble().push([(37,37)]).circle(39,mode='s').finalize().extrude(-50).union(w0.sketch().segment((20,16),(30,16)).segment((30,4)).segment((74,4)).segment((74,16)).segment((84,16)).segment((84,18)).arc((100,53),(84,89)).segment((84,93)).segment((74,93)).segment((74,100)).segment((30,100)).segment((30,93)).segment((20,93)).segment((20,89)).arc((3,53),(20,18)).close().assemble().finalize().extrude(10)).union(w1.sketch().push([(40,37)]).circle(42).circle(36,mode='s').finalize().extrude(-4))
