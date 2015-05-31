import simplekml
import xml.etree.ElementTree as etree
import os

def process_file(f_str):
    doc = etree.ElementTree(file=f_str)
    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    tps = []
    coords = []
    try:
        tps = doc.findall('ns:Activities/ns:Activity', namespaces=ns)[0]\
            .findall('ns:Lap', namespaces=ns)[0]\
            .findall('ns:Track', namespaces=ns)[0]\
            .findall('ns:Trackpoint', namespaces=ns)
    except IndexError:
        # Things like machine workouts don't have paths.
        pass

    coords = []
    for i in tps:
        lat = i.find('ns:Position/ns:LatitudeDegrees', namespaces=ns)\
            .text.strip()
        long = i.find('ns:Position/ns:LongitudeDegrees', namespaces=ns)\
            .text.strip()

        coords.append((long, lat))

    return coords

kml = simplekml.Kml()
script_path = os.path.dirname(os.path.realpath(__file__))
tcx_dir = os.path.join(script_path, 'tcx_files')
lines = []
for i in os.listdir(tcx_dir):
    coords = process_file(os.path.join(tcx_dir, i))
    if not coords:
        continue
    ls = kml.newlinestring(name=i[:-4])
    ls.coords = coords
    ls.extrude = 1
    ls.altitudemode = simplekml.AltitudeMode.relativetoground
    ls.style.linestyle.width = 5
    ls.style.linestyle.color = simplekml.Color.blue

kml.save(os.path.join(script_path, 'out.kml'))
