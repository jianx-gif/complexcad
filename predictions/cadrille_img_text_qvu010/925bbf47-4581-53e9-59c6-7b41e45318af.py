import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-7,0))
r=w0.sketch().segment((-51,-46),(-32,-41)).arc((-42,-41),(-51,-46)).assemble().reset().face(w0.sketch().segment((32,1),(51,46)).arc((42,26),(32,10)).close().assemble()).finalize().extrude(200).union(w1.sketch().segment((-89,67),(-69,67)).segment((-69,-53)).segment((89,-53)).segment((89,53)).segment((-89,53)).close().assemble().push([(0,1)]).circle(48,mode='s').finalize().extrude(16))