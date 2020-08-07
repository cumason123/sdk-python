import pkg_resources
import os

# FORMAT: 1.x.x
_LOCAL_PYPI_VERSION = "1.1.1"
PACKAGE_NAME = "cloudevents"


def createTag():
    from git import Repo

    # metadata.version only works on python3.8
    # Make sure to install most updated version of package
    published_pypi_version = pkg_resources.get_distribution(
        PACKAGE_NAME
    ).version

    # Check pypi and local package version match
    if _LOCAL_PYPI_VERSION == published_pypi_version:
        # Create tag
        repo = Repo(os.getcwd())
        repo.create_tag(_LOCAL_PYPI_VERSION)

        # Push tag to origin master
        origin = repo.remote()
        origin.push(_LOCAL_PYPI_VERSION)

    else:
        # PyPI publish likely failed
        print(
            f"Expected {PACKAGE_NAME}=={_LOCAL_PYPI_VERSION} but found "
            f"{PACKAGE_NAME}=={published_pypi_version}"
        )
        exit(1)


if __name__ == "__main__":
    createTag()
