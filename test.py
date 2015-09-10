from geodata import get_geodata


geodata = get_geodata("127.0.0.1")

print geodata
print str(geodata.get("city"))
