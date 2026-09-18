import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-38,0,0))
r=w0.sketch().arc((-74,-64),(-58,-57),(-42,-53)).arc((-59,-55),(-74,-64)).assemble().reset().face(w0.sketch().arc((-31,90),(19,35),(34,-38)).arc((51,54),(-31,90)).assemble()).finalize().extrude(200).union(w1.sketch().push([(-10,-19)]).circle(81).circle(73,mode='s').finalize().extrude(94))