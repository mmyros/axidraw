from importlib import import_module
import sys

module_names = {
    'axidrawinternal':  [
        'axidraw',
        'axidraw_conf',
        'axidraw_control',
        'axidraw_options',
        'axidraw_svg_reorder',
    ],
    'plotink': [
        'ebb_motion',
        'ebb_serial',
        'plot_utils',
        'plot_utils_import',
    ],
}

def main():
    for supermodule_name, submodule_names in module_names.items():
        for name in submodule_names:
            try:
                sys.modules[__name__].__dict__[name] = alias_submodule(supermodule_name, name)
            except ImportError as ie:
                if "hta" in str(ie) or "axidraw_merge" in str(ie):
                    # this is probably ok, because it just means hershey advanced is not available on this installation
                    pass
                else:
                    raise ie

def alias_submodule(supermodule_name, submodule_name):
    '''
    Note: according to this discussion (https://stackoverflow.com/questions/24322927/python-how-to-alias-module-name-rename-with-preserving-backward-compatibility) this won't work if the submodules go more than two levels deep (i.e. module.submodule.submodule.submodule).
    However, I can't reproduce that and given our existing package structure, I think that's unlikely anyway, and this is simpler than the given full solution.
    '''

    full_name = ".".join([supermodule_name, submodule_name])
    __import__(full_name)
    sys.modules[".".join([__name__, submodule_name])] = sys.modules[full_name]
    return sys.modules[full_name]

main()
