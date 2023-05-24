from os import PathLike
from typing import Dict, List
from ripgrepy import Ripgrepy
from progress.bar import Bar
from jinja2 import Template

class PatternAbstractor:
    directory = ""
    pattern = ""
    extension = ""
    debug = False

    def __init__(
        self, directory: PathLike, pattern: str, extension: str, debug: bool = False
    ) -> None:
        """
        Initializes an instance of the PatternAbstractor class.

        Args:
        - directory (PathLike): The directory to search for files.
        - pattern (str): The regular expression pattern to search for.
        - extension (str): The file extension to search for.
        - debug (bool, optional): Whether or not to enable debug mode. Defaults to False.
        """
        self.directory = directory
        self.pattern = pattern
        self.extension = extension
        self.debug = debug

    def get_matches(self) -> List[Dict]:
        """
        Searches for files in the specified directory that match the specified pattern and extension.

        Returns:
        - List[Dict]: A list of dictionaries containing information about the matches found.
        """
        rg = (
            Ripgrepy(self.pattern, str(self.directory))
            .i()
            .with_filename()
            .line_number()
            .no_heading()
            .glob(f"**/*.{self.extension}")
            .json()
        )
        results = rg.run().as_dict
        return results

    def write_matches_to_template(
        self, matches: List[Dict], template: Template, output_file: PathLike
    ) -> bool:
        """
        Writes the matches found to the specified output file using the specified template.

        Args:
        - matches (List[Dict]): A list of dictionaries containing information about the matches found.
        - template (Template): The Jinja2 template to use for formatting the output.
        - output_file (PathLike): The file to write the output to.

        Returns:
        - bool: True if the output was successfully written to the file, False otherwise.
        """
        try:
            with open(output_file, "w") as outfile:
                bar = None
                if self.debug:
                    bar = Bar("Processing Matches", max=len(matches))
                    bar.start()

                outputs = []
                for res in matches:
                    match = res["data"]
                    file_path = match["path"]["text"]
                    line_number = match["line_number"]
                    line_content = match["lines"]["text"]

                    for submatch in match["submatches"]:
                        text = submatch["match"]["text"]
                        match_start_index = submatch["start"]
                        match_end_index = submatch["end"]

                        outputs.append(
                            {
                                "file_path": file_path,
                                "line_number": line_number,
                                "line_content": line_content,
                                "text": text,
                                "match_start_index": match_start_index,
                                "match_end_index": match_end_index,
                            }
                        )
                    if bar:
                        bar.next()

                outfile.write(template.render(matches=outputs))
                if bar:
                    bar.finish()
            return True

        except FileNotFoundError:
            print(f"ERROR: Could not edit or create output_file {output_file}")
            return False
