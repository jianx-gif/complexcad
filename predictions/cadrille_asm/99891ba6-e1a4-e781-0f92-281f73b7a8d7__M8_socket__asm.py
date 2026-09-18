parts = [base]
parts.append(place(fastener("washer", 'M5', 0), axis=(0, 0, 1), point=(-18, -20, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 10, 0), axis=(0, 0, 1), point=(-18, -20, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(-18, -20, 2.5), seat=-2.5, flip=True))
