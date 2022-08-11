import argparse
import sys

from . import vendorize_requirement, vendorize_requirements

parser = argparse.ArgumentParser()
parser.add_argument(
    "path_or_requirement",
    nargs="?",
    help="path to the TOML configuration file, or a requirement",
)
parser.add_argument(
    "target_directory", nargs="?", help="the directory to put the vendorized package in"
)
parser.add_argument(
    "--top-level-names",
    help="if the distribution of the package being vendored does not contain a "
    "top_level.txt file, a comma-separate list of top level names can be specified here. The top level names "
    "are used to rewrite absolute import statements (only if target_directory is only specified).",
)


def main():
    args = parser.parse_args()
    if args.target_directory is None:
        if args.top_level_names:
            parser.error(
                "--top-level-names can only be used if a single requirement is vendored"
            )
        vendorize_requirements(path=args.path_or_requirement or "vendorize.toml")
    else:
        top_level_names = args.top_level_names.split(",") if args.top_level_names else None
        vendorize_requirement(
            cwd=".",
            requirement=args.path_or_requirement,
            target_directory=args.target_directory,
            top_level_names=top_level_names,
        )


if __name__ == "__main__":
    main()
