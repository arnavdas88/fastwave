import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "src/fastwave/",
    "src/fastwave.examples/",
)


@nox.session()
def format(session):
    session.install("black", "isort")

    session.run("isort", "--profile=black", *SOURCE_FILES)
    session.run("black", "--target-version=py39", *SOURCE_FILES)


@nox.session()
def tests(session):
    pass
