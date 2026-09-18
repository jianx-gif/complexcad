import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-100,-63),(100,-62)).segment((100,63)).segment((-100,62)).segment((-100,46)).segment((-50,35)).segment((-50,-34)).segment((-100,-24)).close().assemble().rect(100,82,mode='s').finalize().extrude(-20)