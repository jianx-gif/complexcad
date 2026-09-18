import cadquery as cq
w0=cq.Workplane('YZ',origin=(-87,0,0))
w1=cq.Workplane('ZX',origin=(0,47,0))
r=w0.sketch().arc((-77,-15),(-65,-11),(-53,-7)).segment((-53,7)).segment((-38,7)).arc((-28,11),(-18,13)).segment((-18,7)).segment((18,7)).segment((18,13)).arc((28,11),(38,7)).segment((42,7)).arc((55,10),(70,12)).arc((65,15),(60,17)).segment((60,100)).segment((-60,100)).segment((-60,17)).arc((-70,2),(-77,-15)).assemble().finalize().extrude(187).union(w1.sketch().arc((-38,-53),(-24,-38),(-10,-24)).arc((-25,-36),(-38,-46)).close().assemble().finalize().extrude(-33))