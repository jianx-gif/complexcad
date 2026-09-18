import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,23))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().segment((-28,-10),(-22,-20)).segment((28,-8)).segment((22,20)).segment((-1,15)).segment((-1,2)).segment((-15,2)).close().assemble().finalize().extrude(-23).union(w0.sketch().push([(0,-1)]).circle(29).circle(20,mode='s').finalize().extrude(-22)).union(w1.sketch().arc((-19,-24),(0,-30),(19,-24)).close().assemble().finalize().extrude(-31))
