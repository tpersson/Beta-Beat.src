from __future__ import print_function
import logging
from madx import madx_wrapper

LOGGER = logging.getLogger(__name__)


class ModelCreator(object):

    @classmethod
    def create_model(creator, instance, output_path, **kwargs):
        instance.verify_object()
        madx_script = creator.get_madx_script(
            instance,
            output_path
        )
        creator.prepare_run(instance, output_path)
        writeto = None
        if "writeto" in kwargs:
            writeto = kwargs["writeto"]
        logfile = None
        if "logfile" in kwargs:
            logfile = kwargs["logfile"]
        creator.run_madx(madx_script, logfile, writeto)

    @classmethod
    def prepare_run(cls, lhc_instance, output_path):
        pass

    @staticmethod
    def run_madx(madx_script, logfile=None, writeto=None):
        madx_wrapper.resolve_and_run_string(
            madx_script,
            output_file=writeto,
            log_file=logfile
        )


class ModelCreationError(Exception):
    """
    Raised when an error happens during model creation.
    """
    pass
