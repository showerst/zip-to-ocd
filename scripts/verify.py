# confirm that all US zips are represented at least once in the output files

import csv

seen_zips_sldu = set()
seen_zips_sldl = set()
seen_zips_cd = set()
seen_zips_state = set()
zips_with_no_lower = set()

with open('sld.csv') as cfile:
    csvfile = csv.reader(cfile, delimiter=',')
    next(csvfile)
    for line in csvfile:

        if line[2][0:4] == 'sldl':
            seen_zips_sldl.add(line[0])
        elif line[2][0:4] == 'sldu':
            seen_zips_sldu.add(line[0])
        else:
            print("WTF: {}".format(line[2]))

        if 'state:ne' in line[1] or 'district:dc' in line[1]:
            zips_with_no_lower.add(line[0])

with open('cd.csv') as cfile:
    csvfile = csv.reader(cfile, delimiter=',')
    next(csvfile)
    for line in csvfile:
        if 'cd:' in line[1]:
            seen_zips_cd.add(line[0])
        else:
            seen_zips_state.add(line[0])

print(seen_zips_cd)

# ignore the zips from the territories
ignored_zips = set()
for i in range(96910, 96933):
    ignored_zips.add( str(i))

for i in range(96950, 96953):
    ignored_zips.add(str(i))

for i in range(800, 852):
    ignored_zips.add(str(i).zfill(5))

ignored_zips.add(str(96799))


dc_zips = set()
for span in [[20001,20039], [20042,20059],[20500, 20600],[20799,20799]]:
    for i in range(span[0], span[1]):
        dc_zips.add(i)

print( dc_zips)


# 2017_Gaz_zcta_national is the master list of census zip codes
# https://www.census.gov/geo/maps-data/data/gazetteer2017.html
with open('scripts/2017_Gaz_zcta_national.txt') as cfile:
    csvfile = csv.reader(cfile, delimiter='\t')
    next(csvfile)
    for line in csvfile:

        zip_code = line[0]

        if zip_code in ignored_zips:
            continue

        if line[0] not in seen_zips_sldl and line[0] not in zips_with_no_lower:
            print("{} not found in lowers".format(line[0]))
        if line[0] not in seen_zips_sldu:
            print("{} not found in uppers".format(line[0]))
        if line[0] not in seen_zips_cd and line[0] not in dc_zips:
            print("{} not found in congressional".format(line[0]))
        if line[0] not in seen_zips_state and line[0] not in dc_zips:
            print("{} not found in us senate".format(line[0]))