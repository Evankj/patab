# patab 
**Pat**tern **Ab**stractor.

This tool is designed to speed up the process of finding pattern matches, abstracting those matches by replacing them with variable names or similar, and finally generating any necessary files.

## Why does this exist?
This tool exists to assist with tasks that may otherwise be time-consuming or involve stringing together a number of command line tools via piping or similar.

## Usage
`python patab.py [-h] [--directory DIRECTORY] --pattern PATTERN --extension EXTENSION [--output-file OUTPUT_FILE] [--context CONTEXT] --template TEMPLATE [--verbose]`

### Arguments
- `--directory (-d)` (default `.`): The directory in which to conduct the search.
- `--pattern (-p)` (required): The pattern to search for.
- `--extension (-e)` (required): The file extension to search for patterns in.
- `--output-file (-o)` (required): The file to write the results to (this will be formatted based on the provided `template`)
- `--template (-t)` (required): Jinja2 template file to populate with found matches.
- `--context (-c)` (default `0`): The number of lines either side of the line on which the pattern was found to include in the output.
- `--verbose (-v)`: Report progress to `stdout`.
 
### Template Files
`patab` will use the provided template file to generate an output file.

The data exposed to this template file consists of a list of `dicts` for each match with the following properties:

 - `file_path`: The path to the file in which the match was found
 - `line_number`: The line number on which the match was found
 - `line_content`: The content of the line on which the match was found
 - `text`: The text inside the match itself
 - `match_start_index`: The index for the character inside `line_content` at which the match starts
 - `match_end_index`: The index for the character inside `line_content` at which the match ends

### Example
`python patab.py --directory /path/to/directory --pattern "error" --extension "log" --output-file "error_matches.json" --context 2 --template "error_template.json.j2" --verbose`

This will search for the pattern `“error”` in all files with the extension `.log` under the directory `/path/to/directory`, and generate a file named `error_matches.json` populated with the found matches using the provided Jinja2 template `error_template.json.j2`. The output will include 2 lines before and after the line on which the match was found, and progress will be reported to stdout.

