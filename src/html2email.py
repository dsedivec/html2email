#!/usr/bin/env python3

import argparse
import sys

import lxml.etree
import lxml.html
import premailer


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("--output", "-o", default=sys.stdout.buffer)
    parser.add_argument("input", nargs="?", default=sys.stdin.buffer)
    args = parser.parse_args(argv[1:])
    tree = lxml.html.parse(args.input)
    # Skylighting, the library used by Pandoc to highlight code, puts
    # <a> at the beginning of each line, even when you're not using
    # line numbers.  Mail.app then makes the whole line look like a
    # link because it's a FUCKER.
    for elem in tree.xpath("//div/pre/code/span/a[@aria-hidden='true']"):
        elem.drop_tag()
    # It seems like we really have to inline all CSS, at least for
    # Mail.app to be happy with Pandoc+Skylighter output in
    # highlighted code blocks.
    premailer.transform(tree.getroot())
    # Completely non-standard type="cite" needed on <blockquote> if
    # you want Mail.app to make it look like a quote.
    for elem in tree.iter("blockquote"):
        if "type" not in elem.attrib:
            elem.attrib["type"] = "cite"
    tree.write(args.output)


if __name__ == "__main__":
    main()
