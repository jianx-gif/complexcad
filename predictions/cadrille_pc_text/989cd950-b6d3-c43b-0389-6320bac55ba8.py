import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-38,-24),(35,-24)).segment((38,24)).segment((-35,24)).close().assemble().circle(19,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-24,14),(-21,-15)).segment((24,-14)).segment((21,16)).close().assemble().circle(10,mode='s').finalize().extrude(-59))