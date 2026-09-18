import cadquery as cq
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-80,-57),(-77,-57)).segment((-77,-60)).segment((77,-60)).segment((77,-57)).segment((80,-57)).segment((80,57)).segment((77,57)).segment((77,60)).segment((-77,60)).segment((-77,57)).segment((-80,57)).close().assemble().rect(150,100,mode='s').finalize().extrude(-200)