import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-69,-61),(-61,-57),(-65,-65)).arc((67,54),(-69,-61)).assemble().reset().face(w0.sketch().segment((-31,-66),(-28,-68)).segment((-24,-62)).arc((60,-47),(59,39)).segment((63,45)).segment((60,47)).segment((56,41)).arc((-38,26),(-30,-61)).close().assemble(),mode='s').finalize().extrude(-200)