import cadquery as cq
w0=cq.Workplane('YZ',origin=(-96,0,0))
w1=cq.Workplane('XY',origin=(0,0,-97))
r=w0.sketch().arc((-56,-51),(-45,-49),(-34,-46)).segment((-44,-46)).segment((-44,-28)).close().assemble().reset().face(w0.sketch().arc((-2,-45),(1,-45),(4,-44)).segment((56,-65)).arc((56,-55),(58,-45)).close().assemble()).reset().face(w0.sketch().segment((34,65),(44,65)).segment((44,46)).segment((56,51)).arc((47,59),(34,65)).assemble()).finalize().extrude(166).union(w1.sketch().segment((-71,1),(21,1)).arc((-25,25),(-71,1)).assemble().finalize().extrude(197))