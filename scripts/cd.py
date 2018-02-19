import csv
import urllib.request
import codecs
import us

states_to_skip = ['AS','PI','GU','MP','VI','AK','DC','PR','DE','MT','ND','SD','VT','WY']
at_large_ranges = {'AK':[[99501,99951]],
                    'DE':[[19701,19981]],
                    'MT':[[59001,59938]],
                    'ND':[[58001,58857]],
                    'SD':[[57001,57800]],
                    'VT':[[5001,5496],[5601,5908]],
                    'WY':[[82001,83129]],
                }

states = us.states.mapping('abbr', 'fips')
print(states)

zip_to_ocd_mapping = []

seen_zips = set()


def get_url(fips, series):
    if series == '115th':
        return "https://www2.census.gov/geo/relfiles/cdsld16/{}/zc_cd_delim_{}.txt".format(str(fips), str(fips))
    elif series == '113th':
        return "https://www2.census.gov/geo/relfiles/cdsld13/{}/zc_cd_delim_{}.txt".format(str(fips), str(fips))



for state in states:
    abbr = state.lower()
    fips = states[state]

    if fips and state not in states_to_skip:


        url_2017 = get_url(fips, '115th')
        print('fetching {}'.format(url_2017))

        try:
            data = urllib.request.urlopen(url_2017)
        except Exception:
            url_2015 = get_url(fips, '113th')
            print('fetching 113th {}'.format(url_2015))

            data = urllib.request.urlopen(url_2015)


        csvfile = csv.reader(codecs.iterdecode(data, 'utf-8'))

        # skip 2 header rows
        next(csvfile)
        next(csvfile)

        for line in csvfile:
            zip_code = line[1]

            if zip_code:
                # ocd-division/country:us/state:al/cd:1
                cd_ocd_id = 'ocd-division/country:us/state:{}/cd:{}'.format( abbr, str(int(line[2])) )
                zip_to_ocd_mapping.append([zip_code, cd_ocd_id])

                if zip_code not in seen_zips:
                    senate_ocd_id = 'ocd-division/country:us/state:{}'.format(abbr)
                    zip_to_ocd_mapping.append([zip_code, senate_ocd_id])
                    seen_zips.add(zip_code)

for abbr in at_large_ranges:
    ranges = at_large_ranges[abbr]
    for span in ranges:
        print(span)
        for zip_code in range(span[0], span[1]):
            cd_ocd_id = 'ocd-division/country:us/state:{}/cd:1'.format( abbr )
            zip_to_ocd_mapping.append([zip_code, cd_ocd_id])

            senate_ocd_id = 'ocd-division/country:us/state:{}'.format(abbr)
            zip_to_ocd_mapping.append([zip_code, senate_ocd_id])



print(zip_to_ocd_mapping)

filename = 'cd.csv'
f = open(filename, 'w')
write_outfile = csv.writer(f)

write_outfile.writerow(['zip','ocd'])
for line in zip_to_ocd_mapping:
    write_outfile.writerow([line[0], line[1]])