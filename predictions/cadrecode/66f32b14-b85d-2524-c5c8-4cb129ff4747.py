import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().rect(200,200).reset().face(w0.sketch().segment((-99,-8),(-38,-8)).arc((0,-38),(38,-8)).segment((99,-8)).segment((99,7)).segment((38,7)).arc((0,37),(-38,7)).segment((-99,7)).close().assemble(),mode='s').push([(25,76)]).circle(7,mode='s').push([(71,-75)]).circle(7,mode='s').finalize().extrude(-12)