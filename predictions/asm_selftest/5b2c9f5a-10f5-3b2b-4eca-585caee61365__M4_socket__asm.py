parts = [base]
parts.append(place(fastener("washer", 'M8', 0), axis=(0, 0, 1), point=(0, 0, 2), seat=1.9, flip=False))
parts.append(place(fastener("screw", 'M8-1.25', 14, 0), axis=(0, 0, 1), point=(0, 0, 2), seat=3.7, flip=False))
parts.append(place(fastener("nut", 'M8-1.25', 'M8', 0), axis=(0, 0, 1), point=(0, 0, 2), seat=-2, flip=True))
