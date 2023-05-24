import argparse
from os import error
from ripgrepy import Ripgrepy
from progress.bar import Bar
from jinja2 import Template
from patab import PatternAbstractor

parser = argparse.ArgumentParser(
    description="Search for a pattern in files with a given extension under a directory"
)
parser.add_argument(
    "--directory", "-d", default=".", help="the directory to search in", type=str
)
parser.add_argument(
    "--pattern", "-p", required=True, help="the pattern to search for", type=str
)
parser.add_argument(
    "--extension",
    "-e",
    required=True,
    help="the file extension to search for",
    type=str,
)
parser.add_argument(
    "--output-file",
    "-o",
    default="matches.csv",
    help="the CSV file to write the results to",
    type=str,
)
parser.add_argument(
    "--context",
    "-c",
    default=1,
    help="the number of lines before and after the line on which the match was found to include",
    type=int,
)
parser.add_argument(
    "--template",
    "-t",
    required=True,
    help="Jinja2 template file to populate with found matches",
    type=str,
)
parser.add_argument(
    "--verbose", "-v", help="report progress to stdout", action="store_true"
)
args = parser.parse_args()


def cli() -> bool:
    """
    Command line interface for running the pattern abstractor.

    Returns:
    - bool: True if the output was successfully written to the file, False otherwise.
    """
    patab = PatternAbstractor(
        directory=args.directory,
        pattern=args.pattern,
        extension=args.extension,
        debug=args.verbose,
    )
    matches = patab.get_matches()
    template: Template | None = None
    try:
        with open(args.template) as templatefile:
            template = Template(templatefile.read())
    except:
        """
        Catches errors when trying to read the template file and prints an error message.

        Args:
        - args.template (str): The name of the template file that could not be read.

        Returns:
        - bool: False, indicating that the output was not successfully written to the file.
        """
        print(
            f"ERROR: Could not initialise template from template file: {args.template}"
        )
        return False

    patab.write_matches_to_template(
        matches=matches, template=template, output_file=args.output_file
    )
    return True


if __name__ == "__main__":
    """
    Runs the command line interface and prints a success message if the output was successfully written to the file.
    """
    if cli():
        print(f"Template file {args.output_file} successfully generated...")
    else:
        print("Something went wrong! Exiting...")
