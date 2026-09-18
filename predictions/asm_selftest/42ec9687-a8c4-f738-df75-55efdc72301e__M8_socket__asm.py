parts = [base]
parts.append(place(fastener("washer", 'M8', 0), axis=(0, 0, 1), point=(10, 45, 4), seat=3.8, flip=False))
parts.append(place(fastener("screw", 'M8-1.25', 18, 0), axis=(0, 0, 1), point=(10, 45, 4), seat=5.6, flip=False))
parts.append(place(fastener("nut", 'M8-1.25', 'M8', 0), axis=(0, 0, 1), point=(10, 45, 4), seat=-4, flip=True))
