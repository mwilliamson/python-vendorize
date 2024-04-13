import sys

from . import vendorize_directory, vendorize_requirement, vendorize_requirements


def main():
    if len(sys.argv) < 2:
        vendorize_directory(".")
    elif len(sys.argv) < 3:
        vendorize_requirements(path=sys.argv[1])
    else:
        requirement = sys.argv[1]
        target_directory = sys.argv[2]
        vendorize_requirement(cwd=".", requirement=requirement, target_directory=target_directory)


if __name__ == "__main__":
    main()
