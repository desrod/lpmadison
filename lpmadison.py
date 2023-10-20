#!/usr/bin/env python3

import argparse

import pendulum
from launchpadlib.launchpad import Launchpad

INSTANCE = "production"
VALID_API_VERSIONS = ("beta", "1.0", "devel")
API_VERSION = "devel"


def get_published_binaries(series_name, arch=None, package=None):
    launchpad = Launchpad.login_anonymously("ubuntu", INSTANCE, version=API_VERSION)
    ubuntu = launchpad.distributions["ubuntu"]
    archive = ubuntu.main_archive
    series = ubuntu.getSeries(name_or_version=series_name)

    package_args = {"exact_match": True}

    if arch:
        package_args["distro_arch_series"] = series.getDistroArchSeries(archtag=arch)
    if package:
        package_args["binary_name"] = package

    return archive.getPublishedBinaries(**package_args)


def display_packages(packages, lineout=False):
    now = pendulum.now()
    for p in packages:
        publish_date = pendulum.parse(str(p.date_published))
        delta = now - publish_date

        if lineout:
            print(f"{p.date_published} {p.source_package_name} {p.source_package_version} {p.binaryFileUrls()}")
        else:
            print_package_details(p, delta)

def parse_repo(args):
    series = getattr(args, "series", None)
    arch = getattr(args, "arch", None)
    package = getattr(args, "package", None)
    lineout = getattr(args, "lineout", False)

    packages = get_published_binaries(series, arch, package)
    display_packages(packages, lineout)


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
        action="store_true",
        help="Produce line-oriented output instead of the default stanza-oriented output",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.series:
        parse_repo(args)


if __name__ == "__main__":
    main()
