# zip-to-ocd
Mappings of US Zip codes to OpenCivicData Identifiers

Warning: [Zip Codes are a terrible way to map to jurisdictions](https://sunlightfoundation.com/2012/01/19/dont-use-zipcodes/). They are non-contiguous, poorly defined, and can map to multiple jursidctions. Whenever possible, geocode a real address and lookup by lat/lon.

## Usage:
cd.csv contains:
 * one line for each zip code to each US Congressional district that at least partially overlaps it
 * and one line for the state containing it.

sld.csv contains
 * one line for each zip code to each state lower-house congressional district (sldl) at least partially overlapping it, except Nebraska, which has no lower house.
 * one line for each zip code to each state Senate district (sldu) at least partially overlapping it.
 * the FIPS code for the district
 * the minimum valid date for the combination

scripts contains
* the census list of US zip codes
* scripts to download the census files and generate cd.csv and sld.csv
* a basic verification script to check that all zips are present at least once in all data sets, excepting ignored zips from US territories

 [OpenCivicData identifiers](http://opencivicdata.readthedocs.io/en/latest/ocdids.html) are a standardized identifier format for political divisions and areas of interest.  [Documentation](http://opencivicdata.readthedocs.io/en/latest/ocdids.html) [Full list and code](https://github.com/opencivicdata/ocd-division-ids)
