import cadquery as cq
w0=cq.Workplane('YZ',origin=(-14,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().push([(0,1)]).circle(99).circle(65,mode='s').finalize().extrude(64).union(w1.sketch().arc((-96,-31),(0,-82),(96,-31)).segment((96,-30)).arc((100,1),(96,30)).segment((96,31)).arc((54,59),(13,82)).arc((10,82),(7,83)).arc((-1,84),(-9,84)).arc((-16,83),(-23,82)).arc((-61,46),(-67,-4)).arc((-69,-1),(-70,2)).segment((-70,-31)).close().assemble().finalize().extrude(200))