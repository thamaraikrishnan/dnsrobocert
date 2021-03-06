#!/usr/bin/env python3
import argparse
import importlib
import os

from lexicon import discovery


def main():
    providers = [
        provider for provider in discovery.find_providers().keys() if provider != "auto"
    ]

    output = """\
=========================
Lexicon providers options
=========================

Supported providers
===================

The following Lexicon providers are supported by DNSroboCert.

{0}

Providers options
=================

""".format(
        _generate_table(["{0}_".format(provider) for provider in providers])
    )

    for provider in providers:
        provider_module = importlib.import_module("lexicon.providers." + provider)
        parser = argparse.ArgumentParser()
        provider_module.provider_parser(parser)

        output = (
            output
            + """\
.. _{0}:

{0}
""".format(
                provider
            )
        )

        for action in parser._actions:
            if action.dest == "help":
                continue

            output = (
                output
                + """\
    * ``{0}`` {1}
""".format(
                    action.dest, action.help.capitalize().replace("`", "'")
                )
            )

        output = output + "\n"

    with open(os.path.join("docs", "providers_options.rst"), "w") as f:
        f.write(output)


def _generate_table(items):
    nb_colums = 4
    table = []
    max_width = max(len(item) for item in items) + 1
    delimitator = "+{0}+".format("+".join(["-" * max_width] * nb_colums))

    table.append(delimitator)

    normalized = [
        "{0}{1}".format(item, " " * (max_width - len(item))) for item in items
    ]
    divided = [
        normalized[n : n + nb_colums] for n in range(0, len(normalized), nb_colums)
    ]

    for division in divided:
        entry = [*division, *[" " * max_width] * (nb_colums - len(division))]
        line = "|{0}|".format("|".join(entry))
        table.append(line)
        table.append(delimitator)

    return "\n".join(table)


if __name__ == "__main__":
    main()
