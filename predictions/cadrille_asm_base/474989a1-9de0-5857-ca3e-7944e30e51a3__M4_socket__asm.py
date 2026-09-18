import cadquery as cq
w0=cq.Workplane('YZ',origin=(81,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-6),(-52,-23)).segment((-31,6)).segment((-54,23)).close().assemble().finalize().extrude(-166).union(w1.sketch().segment((-71,-9),(70,-9)).segment((70,-8)).arc((75,0),(70,8)).segment((70,10)).segment((-71,10)).close().assemble().push([(-26,7.5)]).rect(12,3,mode='s').push([(24,4)]).rect(10,4,mode='s').finalize().extrude(-200))