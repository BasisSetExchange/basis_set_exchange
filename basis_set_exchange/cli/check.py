'''
Validators for command line options
'''

import os
import copy
from .. import api


def _cli_check_data_dir(data_dir):
    '''Checks that the data dir exists and contains METADATA.json'''

    if data_dir is None:
        return None

    data_dir = os.path.expanduser(data_dir)
    data_dir = os.path.expandvars(data_dir)
    if not os.path.isdir(data_dir):
        raise RuntimeError("Data directory '{}' does not exist or is not a directory".format(data_dir))
    if not os.path.isfile(os.path.join(data_dir, 'METADATA.json')):
        raise RuntimeError("Data directory '{}' does not contain a METADATA.json file".format(data_dir))

    return data_dir


def _cli_check_format(fmt):
    '''Checks that a basis set format exists and if not, raises a helpful exception'''

    if fmt is None:
        return None

    fmt = fmt.lower()
    if not fmt in api.get_formats():
        errstr = "Format '" + fmt + "' does not exist.\n"
        errstr += "For a complete list of formats, use the 'list-formats' subcommand"
        raise RuntimeError(errstr)

    return fmt


def _cli_check_ref_format(fmt):
    '''Checks that a reference format exists and if not, raises a helpful exception'''

    if fmt is None:
        return None

    fmt = fmt.lower()
    if not fmt in api.get_reference_formats():
        errstr = "Reference format '" + fmt + "' does not exist.\n"
        errstr += "For a complete list of formats, use the 'list-ref-formats' subcommand"
        raise RuntimeError(errstr)

    return fmt


def _cli_check_role(role):
    '''Checks that a basis set role exists and if not, raises a helpful exception'''

    if role is None:
        return None

    role = role.lower()
    if not role in api.get_roles():
        errstr = "Role format '" + role + "' does not exist.\n"
        errstr += "For a complete list of roles, use the 'list-roles' subcommand"
        raise RuntimeError(errstr)

    return role


def _cli_check_basis(name, data_dir):
    '''Checks that a basis set exists and if not, raises a helpful exception'''

    if name is None:
        return None

    name = name.lower()
    metadata = api.get_metadata(data_dir)
    if not name in metadata:
        errstr = "Basis set '" + name + "' does not exist.\n"
        errstr += "For a complete list of basis sets, use the 'list-basis-sets' subcommand"
        raise RuntimeError(errstr)

    return name


def _cli_check_family(family, data_dir):
    '''Checks that a basis set family exists and if not, raises a helpful exception'''

    if family is None:
        return None

    family = family.lower()
    if not family in api.get_families(data_dir):
        errstr = "Basis set family '" + family + "' does not exist.\n"
        errstr += "For a complete list of families, use the 'list-families' subcommand"
        raise RuntimeError(errstr)

    return family


def cli_check_normalize_args(args):
    '''Check and normalize arguments
       This function checks that basis set names, families, roles, etc, are
       valid (and raise an exception if they aren't)

       The original data passed to this function is not modified. A modified
       copy is returned.
    '''

    args_keys = vars(args).keys()  # What args we have
    args_copy = copy.copy(args)
    if 'data_dir' in args_keys:
        args_copy.data_dir = _cli_check_data_dir(args.data_dir)
    if 'basis' in args:
        args_copy.basis = _cli_check_basis(args.basis, args.data_dir)
    if 'fmt' in args_keys:
        args_copy.fmt = _cli_check_format(args.fmt)
    if 'reffmt' in args_keys:
        args_copy.reffmt = _cli_check_ref_format(args.reffmt)
    if 'role' in args_keys:
        args_copy.role = _cli_check_role(args.role)
    if 'family' in args_keys:
        args_copy.family = _cli_check_family(args.family, args.data_dir)

    return args_copy