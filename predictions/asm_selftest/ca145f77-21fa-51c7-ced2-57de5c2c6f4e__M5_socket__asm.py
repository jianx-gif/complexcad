parts = [base]
parts.append(place(fastener("washer", 'M5', 0), axis=(0, 0, 1), point=(20, 0, 5), seat=5, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 18, 0), axis=(0, 0, 1), point=(20, 0, 5), seat=6.1, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(20, 0, 5), seat=-5, flip=True))
