import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('YZ',origin=(39,0,0))
r=w0.sketch().segment((-41,-37),(59,-38)).segment((59,37)).segment((-38,38)).close().assemble().push([(8.5,0)]).rect(85,60,mode='s').finalize().extrude(-200).union(w1.sketch().segment((-59,21),(-25,21)).arc((-42,34),(-59,21)).assemble().finalize().extrude(-80))