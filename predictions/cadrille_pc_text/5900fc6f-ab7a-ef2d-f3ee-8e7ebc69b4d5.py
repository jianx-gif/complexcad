import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-38,-15),(38,-15)).arc((29,-4),(16,5)).segment((1,34)).segment((-14,15)).arc((-28,-1),(-38,-15)).assemble().push([(0,-1)]).circle(10,mode='s').finalize().extrude(200)