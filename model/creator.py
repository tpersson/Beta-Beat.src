import sys
import os
import argparse

CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, "..")))

import manager  # noqa
from model_creators import model_creator  # noqa
from model_creators.lhc_model_creator import (  # noqa
    LhcModelCreator,
    LhcBestKnowledgeCreator,
    LhcSegmentCreator,
    LhcCouplingCreator,
)


CREATORS = {
    "lhc": {"nominal": LhcModelCreator,
            "best_knowledge": LhcBestKnowledgeCreator,
            "segment": LhcSegmentCreator,
            "coupling_correction": LhcCouplingCreator},
}


def create_model(accel_inst, model_type, output_path, **kwargs):
    CREATORS[accel_inst.NAME][model_type].create_model(
        accel_inst,
        output_path,
        **kwargs
    )


def _i_am_main():
    rest_args = sys.argv[1:]

    accel_cls, rest_args = manager.get_accel_class_from_args(
        rest_args
    )
    accel_inst, rest_args = accel_cls.init_from_args(rest_args)
    options = _parse_rest_args(rest_args)
    create_model(
        accel_inst,
        options.type,
        options.output,
        writeto=options.writeto,
        logfile=options.logfile,
    )


def _parse_rest_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        help="Type of model to create, either nominal or best_knowledge",
        choices=("nominal", "best_knowledge", "coupling_correction"),
    )
    parser.add_argument(
        "--output",
        help="Output path for model, twiss files will be writen here.",
        dest="output",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--writeto",
        help="Path to the file where to write the resulting MAD-X script. ",
        dest="writeto",
        type=str,
    )
    parser.add_argument(
        "--logfile",
        help=("Path to the file where to write the MAD-X script output."
              "If not provided it will be written to sys.stdout."),
        dest="logfile",
        type=str,
    )
    options = parser.parse_args(args)
    return options


if __name__ == "__main__":
    _i_am_main()
