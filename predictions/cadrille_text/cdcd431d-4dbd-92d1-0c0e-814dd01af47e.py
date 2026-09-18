import cadquery as cq
w0=cq.Workplane('XY',origin=(-27,-27,-100))
w1=cq.Workplane('XY',origin=(-23,-23,-100))
r=w0.sketch().face(w0.sketch().segment((0,0),(54,0)).segment((54,0),(54,54)).segment((54,54),(0,54)).segment((0,54),(0,0)).assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(46,0)).segment((46,0),(46,46)).segment((46,46),(0,46)).segment((0,46),(0,0)).assemble()).finalize().extrude(110))