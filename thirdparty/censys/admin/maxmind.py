from __future__ import print_function
import csv
import sys

import netaddr

from ..base import CensysAPIBase


class CensysAdminMaxmind(CensysAPIBase):

    def upload(self, collection, version, records):
        url = "/admin/maxmind/%s/%i" % (collection, version)
        return self._post(url, data={"records": records})

    def delete(self, collection, version):
        url = "/admin/maxmind/%s/%i" % (collection, version)
        return self._delete(url)


def main():
    if len(sys.argv) < 5:
        sys.stderr.write("USAGE: %s collection version locations.csv" \
                         " blocks.csv\n"
                         % sys.argv[0])
        sys.exit(1)
    collection = sys.argv[1]
    version = int(sys.argv[2])
    locations_path = sys.argv[3]
    blocks_path = sys.argv[4]

    censys = CensysAdminMaxmind()

    to_upload = []
    # population dictionary with all the details for a geoid
    locations = {}
    headers = "geoname_id,locale_code,continent_code,continent_name," \
              "country_iso_code,country_name,subdivision_1_iso_code," \
              "subdivision_1_name,subdivision_2_iso_code,subdivision_2_name," \
              "city_name,metro_code,time_zone".split(",")
    with open(locations_path, "r") as fd:
        for row in csv.reader(fd):
            if not row:
                continue
            if row[0].startswith("geoname_id"):
                continue
            d = {k: v for (k, v) in zip(headers, row)}
            locations[row[0]] = d
    # now that all geoid data is in memory, go through ips, generate full
    # records and then upload them in batches to Censys.
    headers = "network,geoname_id,registered_country_geoname_id," \
              "represented_country_geoname_id,is_anonymous_proxy," \
              "is_satellite_provider,postal_code,latitude,longitude".split(",")
    with open(blocks_path, "r") as fd:
        for row in csv.reader(fd):
            if not row:
                continue
            if row[0].startswith("network"):
                continue
            ipdetails = {k: v for (k, v) in zip(headers, row)}
            geoid = row[1]
            if geoid == "":
                geoid = row[2]
            details = locations[geoid]
            cidr = netaddr.IPNetwork(row[0])
            first = int(cidr[0])
            last = int(cidr[-1])
            rec = {"ip_begin": first, "ip_end": last}
            rec.update(ipdetails)
            rec.update(details)
            print(rec)
            to_upload.append(rec)
            if len(to_upload) > 10000:
                censys.upload(collection, version, to_upload)
                to_upload = []
        censys.upload(collection, version, to_upload)


if __name__ == "__main__":
    main()
