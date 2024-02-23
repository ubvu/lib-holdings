# lib-holdings

Command Line Interface (CLI) tool for retrieving holding counts for a list of OCNs and institutes.
Uses the OCLC API: https://developer.api.oclc.org/

## Installation

First of all, you will need to have Python installed on your computer and available on the command line.
If this sounds scary, consider installing the [Anaconda Navigator](https://www.anaconda.com/anaconda-navigator), an application that comes with Python and a command line.

Once installed, find and run the *Anaconda Prompt* which is the command line interface.

Again, knowing the command line is not a requirement. Simply copy the following into the window and press enter:

```bash
pip install lib-holdings
```

After the tool has been installed, continue below to learn how it works.

## Usage

### Preparation 

Make sure you have the two input files ready:

1. A text file (e.g. *.txt*) containing OCNs with 1 OCN per line
2. A text file (e.g. *.txt*) containing institute symbols with 1 symbol per line

It is recommended to create a folder on your computer in which you place these input files.

Note down the path to this folder, e.g. C:/Users/username/myfolder (on Windows).

Execute the following command, replacing PATH with your path:

```bash
cd PATH
```

The command line now has access to that folder.

Create an empty folder (e.g. *out*) in which the results will be stored.

Also, keep your API key and secret handy.

### Run the program

Copy and execute the following command, after replacing the indicated arguments.

(Description of the arguments can be found below)

```bash
holdings [OPTIONS] INFILE_OCNS INFILE_SYMB OUT_FOLDER
```

ARGUMENTS:

    INFILE_OCNS:    name of the text file containing OCNs (1 per line)
    INFILE_SYMB:    name of the text file containing institute symbols (1 per line)
    OUT_FOLDER:     output directory

OPTIONS:
```bash
--start INTEGER  Position of OCN to start with.
--key TEXT       OCLC API key.
--secret TEXT    OCLC API secret.
```

Note:

The *start* option is handy when the program is interrupted or exits with an error.
In that case, you can re-run the program, providing the start value shown.
