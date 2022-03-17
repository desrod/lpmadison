#!/usr/bin/env python3

import argparse
import pendulum
from launchpadlib.launchpad import Launchpad

instance = "production"
valid_api_versions = ("beta", "1.0", "devel")
api_version = "devel"


def parse_repo(args):
    launchpad = Launchpad.login_anonymously("ubuntu", instance, version=api_version)

    ubuntu = launchpad.distributions["ubuntu"]
    archive = ubuntu.main_archive

    # ubuntu = launchpad.distributions["cloud-archive"]
    # archive = ubuntu.cloud_archive

    series = ubuntu.getSeries(name_or_version=args.series)

    #########################################################
    # For Binary
    package_args = {"exact_match": True}

    if args.arch:
        package_args["distro_arch_series"] = series.getDistroArchSeries(
            archtag=args.arch
        )
    if args.package:
        package_args["binary_name"] = args.package

    pkg = archive.getPublishedBinaries(**package_args)

    #########################################################
    # For Sources
    # package_args = {"exact_match": True, "distro_series": series}

    # print(package_args)

    # if args.arch:
    #     print(package_args)
    #     print(series.getDistroArchSeries(archtag=args.arch))

    # if args.package:
    #     package_args["source_name"] = args.package

    if args.date:
        filter_date = args.date

    # pkg = archive.getPublishedSources(**package_args)

    for p in pkg:
        (publish_date, delta) = parse_publish_date(args, p.date_published)

        # if pendulum.parse(args.date).format("YYYY-MM-DD") == publish_date.format(
        #     "YYYY-MM-DD"
        # ):

        print(
            f"Package: '{p.source_package_name}'\n"
            f"\tVersion: '{p.source_package_version}'\n"
            f"\tPublished: '{p.date_published}'\n"
            f"\tDays ago: {delta.in_days()}"
        )
        # f"\tURLs: '{p.binaryFileUrls()}\n"

        for u in p.binaryFileUrls():
            print(f"\t{u}\n")


def parse_publish_date(args, foo):
    now = pendulum.now()

    publish_date = pendulum.parse(str(foo))
    delta = now - publish_date

    return publish_date, delta


def parse_args():
    parser = argparse.ArgumentParser(description="Launchpad Reposoitory Mirror Builder")

    parser.add_argument("--series", help="Search packages in this series")
    parser.add_argument("--arch", help="Limit results to this architecture")
    parser.add_argument("--package", help="Limit search to a specific package")
    parser.add_argument("--version", help="Limit to this specific version or submatch")
    parser.add_argument("--date", help="Search packages published on <date>")
    parser.add_argument("--before", help="Search packages published before <date>")
    parser.add_argument("--after", help="Search packages published after <date>")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.series:
        parse_repo(args)


if __name__ == "__main__":
    main()
