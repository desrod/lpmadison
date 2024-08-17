#!/usr/bin/env python3

import argparse
import pendulum
import sys
from launchpadlib.launchpad import Launchpad

INSTANCE = "production"
VALID_API_VERSIONS = ("beta", "1.0", "devel")
API_VERSION = "devel"


def get_published_binaries(**kwargs):
    launchpad = Launchpad.login_anonymously("ubuntu", INSTANCE, version=API_VERSION)
    ubuntu = launchpad.distributions["ubuntu"]
    archive = ubuntu.main_archive
    series = ubuntu.getSeries(name_or_version=kwargs.get("series"))

    package_args = {"exact_match": True}

    if kwargs.get("arch"):
        package_args["distro_arch_series"] = series.getDistroArchSeries(archtag=kwargs["arch"])
    if kwargs.get("package"):
        package_args["binary_name"] = kwargs["package"]
    if kwargs.get("version"):
        package_args["version"] = kwargs["version"]
    if kwargs.get("date"):
        package_args["created_since_date"] = kwargs.get("date").isoformat()
    if kwargs.get("after"):
        package_args["created_since_date"] = kwargs.get("after").to_date_string()

    return archive.getPublishedBinaries(**package_args)


def display_packages(packages, **kwargs):
    now = pendulum.now()
    for p in packages:
        publish_date = pendulum.parse(str(p.date_published))
        # If not the right date or before certain date, don't print
        if kwargs.get("date") and kwargs.get("date").to_date_string() != publish_date.to_date_string():
            continue
        if kwargs.get("before") and kwargs.get("before") < publish_date:
            continue

        delta = now - publish_date

        if kwargs.get("lineout"):
            print(f"{p.date_published} {p.source_package_name} {p.source_package_version} {p.binaryFileUrls()}")
        else:
            print_package_details(p, delta)


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
    parser.add_argument("-s", "--series", help="Search packages in this series", required=True)
    parser.add_argument("-r", "--arch", help="Limit results to this architecture")
    parser.add_argument("-p", "--package", help="Limit search to a specific package")
    parser.add_argument("-v", "--version", help="Limit to this specific version or submatch")
    parser.add_argument("-d", "--date", help="Search packages published on <date>")
    parser.add_argument("-b", "--before", help="Search packages published before <date>")
    parser.add_argument("-a", "--after", help="Search packages published after <date>")
    parser.add_argument(
        "-l",
        "--lineout",
        action="store_true",
        default=False,
        help="Produce line-oriented output instead of the default stanza-oriented output",
    )

    args = parser.parse_args()
    if args.date and (args.before or args.after):
        print("Argument --date is mutually exclusive with options --before and --after", file=sys.stderr)
        sys.exit(1)

    new_args = vars(args)
    if args.date:
        new_args["date"] = pendulum.parse(args.date)
    if args.before:
        new_args["before"] = pendulum.parse(args.before)
    if args.after:
        # Add a day since we presume after means not including, but the search by default is inclusive
        new_args["after"] = pendulum.parse(args.after).add(days=1)

    return new_args


def main():
    args = parse_args()
    packages = get_published_binaries(**args)
    display_packages(packages, **args)


if __name__ == "__main__":
    main()
