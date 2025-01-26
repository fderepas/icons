import re
import os
import subprocess

tableOfPng="\n"
tableOfPngCount=0;

def clean_string(s):
    """
    Return the result of replacing
    "%3E" and "%3C" by ">" and "<"
    in the supplied string s.
    """
    s1=re.sub("%3E", ">", re.sub("%3C", "<", s))
    s2=re.sub(r"\#\{vf\-url\-friendly\-color\(\$color\)\}","#000000",s1)
    return s2


def parse_file(file_path):
    """
    Reads a file line by line and prints each line.

    Args:
        file_path (str): Path to the file to be parsed.
    """
    global tableOfPng
    global tableOfPngCount
    try:
        with open(file_path, 'r') as scss_file:
            currentName=""
            for num, line in enumerate(scss_file, start=1):
                m = re.match(r"^@function vf\-icon\-(.*)\-url\(",line)
                if m:
                    currentName=m.group(1)
                    print(f"Line {num}:", m.group(1))
                else:
                    m = re.match(r".*@return url\(\"data\:image\/svg\+xml\,(.*)\"\)\;.*",line)
                    if m:
                        # create svg file
                        svgFile=currentName+'.svg'
                        try:
                            with open(svgFile, 'w') as svg_file:
                                svg_file.write(clean_string(m.group(1)))
                        except PermissionError:
                            print(f"Error: Permission denied to write to file '{svgFile}'.")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                        # create png out of svg
                        subprocess.run(["inkscape",
                                        "--export-type=png",
                                        "--export-height=256",
                                        "--export-width=256",
                                        svgFile], capture_output=True)
                        tableOfPng=tableOfPng+"|!["+currentName+"](https://github.com/fderepas/icons/blob/main/img/"+currentName+".png)"
                        tableOfPngCount=tableOfPngCount+1
                        if tableOfPngCount%4 == 0:
                            tableOfPng+="|\n"
                        

    except FileNotFoundError:
        print(f"File not found: {file_path}")


if __name__ == "__main__":
    parse_file('vanilla-framework/scss/_base_icon-definitions.scss')
    htmlFileName="README.md"
    try:
        with open(htmlFileName, 'w') as htmlFile:
            htmlFile.write("This git archive store svg files and png extracted from ```https://github.com/canonical/vanilla-framework.git```.\n\nExtraction is automatic.")
            htmlFile.write(tableOfPng+"|\n")
            htmlFile.write("")
    except PermissionError:
        print(f"Error: Permission denied to write to file '{htmlFileName}'.")
