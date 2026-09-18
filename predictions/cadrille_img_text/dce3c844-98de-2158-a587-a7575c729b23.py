import cadquery as cq
w0=cq.Workplane('YZ',origin=(-74,0,0))
w1=cq.Workplane('ZX',origin=(0,-14,0))
r=w0.sketch().segment((-86,42),(-85,42)).segment((-85,41)).arc((-67,66),(-42,84)).segment((-42,91)).segment((-86,91)).close().assemble().reset().face(w0.sketch().segment((-19,-84),(42,-91)).segment((42,-84)).arc((67,-66),(86,-42)).segment((85,-41)).segment((85,-42)).arc((67,-66),(42,-84)).segment((42,-91)).segment((-19,-91)).close().assemble()).finalize().extrude(174).union(w1.sketch().push([(75,-46)]).circle(25).circle(15,mode='s').finalize().extrude(28))