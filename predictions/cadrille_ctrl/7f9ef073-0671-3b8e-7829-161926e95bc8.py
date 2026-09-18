import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().arc((24,19),(25,13),(25,8)).segment((33,3)).arc((29,12),(24,19)).assemble().finalize().extrude(-40).union(w0.sketch().push([(0,0)]).circle(30).circle(15,mode='s').finalize().extrude(-20)).union(w0.sketch().push([(0,0)]).circle(29).circle(15,mode='s').finalize().extrude(-10))
