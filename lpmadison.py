#!/usr/bin/env python3

import argparse
import pendulum
from launchpadlib.launchpad import Launchpad

INSTANCE = "production"
VALID_API_VERSIONS = ("beta", "1.0", "devel")
API_VERSION = "devel"


def parse_repo(args):
    launchpad = Launchpad.login_anonymously("ubuntu", INSTANCE, version=API_VERSION)
    ubuntu = launchpad.distributions["ubuntu"]
    archive = ubuntu.main_archive
    series = ubuntu.getSeries(name_or_version=args.series)

    package_args = {"exact_match": True}

    if args.arch:
        package_args["distro_arch_series"] = series.getDistroArchSeries(
            archtag=args.arch
        )
    if args.package:
        package_args["binary_name"] = args.package

    pkg = archive.getPublishedBinaries(**package_args)

    for p in pkg:
        publish_date, delta = parse_publish_date(p.date_published)

        if args.lineout:
            print(
                f"{p.date_published} {p.source_package_name} {p.source_package_version} {p.binaryFileUrls()}"
            )
        else:
            print_package_details(p, delta)


def parse_publish_date(date_str):
    now = pendulum.now()
    publish_date = pendulum.parse(str(date_str))
    delta = now - publish_date
    return publish_date, delta


def print_package_details(package, delta):
    print(
        f"Package: '{package.source_package_name}'\n"
        f"\tVersion: '{package.source_package_version}'\n"
        f"\tPublished: '{package.date_published}'\n"
        f"\tDays ago: {delta.in_days()}"
    )
    for url in package.binaryFileUrls():
        print(f"\t{url}\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Launchpad Repository Mirror Builder")
    parser.add_argument("--series", help="Search packages in this series")
    parser.add_argument("--arch", help="Limit results to this architecture")
    parser.add_argument("--package", help="Limit search to a specific package")
    parser.add_argument("--version", help="Limit to this specific version or submatch")
    parser.add_argument("--date", help="Search packages published on <date>")
    parser.add_argument("--before", help="Search packages published before <date>")
    parser.add_argument("--after", help="Search packages published after <date>")
    parser.add_argument(
        "--lineout",
        action='store_true',
        help="Produce line-oriented output instead of the default stanza-oriented output",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.series:
        parse_repo(args)


if __name__ == "__main__":
    main()
