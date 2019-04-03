import re


def validate_version_format(version_str):
    """
    Check if the version format is valid
    :param version_str: Version to check format.
    :return: True: valid | False: invalid
    """
    if version_str is None:
        raise ValueError('Version must not be None')

    if not isinstance(version_str, str):
        raise ValueError('Version must be string')

    return re.fullmatch(r'^[0-9]+(\.[0-9]+)*', version_str) is not None


def validate_and_split_versions(version_1, version_2):
    """
    Validate and split versions into parts.
    :param version_1: Version 1.
    :param version_2: Version 2.
    :return: List of versions splitted into parts.
    """
    splitted_versions = []

    for version in [version_1,version_2]:
        if version is None or version == '':
            raise ValueError('Both versions must not be empty')

        if not validate_version_format(version):
            raise ValueError('Version "{}" is not valid'.format(version))

        splitted_versions.append(version.split("."))

    if len(splitted_versions[0]) != len(splitted_versions[1]):
        raise ValueError('Versions must have the same format mask')

    return splitted_versions


def compare_versions(version_1, version_2):
    """
    Compare two versions.
    :param version_1: Version 1.
    :param version_2: Version 2.
    :return: 0: versions are equals
             1: First version is greater than second one
             2: Second version is greater than first one
    """
    splitted_v1, splitted_v2 = validate_and_split_versions(version_1, version_2)

    for i in range(0, len(splitted_v1)):
        v1_part_int = int(splitted_v1[i])
        v2_part_int = int(splitted_v2[i])

        if v1_part_int < v2_part_int:
            # Second version is greater than first one
            return 2
        elif v1_part_int > v2_part_int:
            # First version is greater than second one
            return 1

    # All parts of the versions are equals
    return 0
