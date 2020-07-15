# checks whether all modules are properly structured, have necessary files and methods present
import importlib
from os import listdir
from os.path import join, abspath, isdir, dirname, isfile

MODULES_PATH = join(abspath(dirname(__file__)), '..', '..', 'nnk', 'modules')


def test_modules_conformance():
    modules = [f for f in listdir(MODULES_PATH)
               if isdir(join(MODULES_PATH, f))]
    modules.remove('templatemodule')  # FIXME temporary fix. templatemodule will be moved elsewhere later on

    for m in modules:
        assert isfile(join(MODULES_PATH, m, m + 'service.py'))
        # check if the folder contains properly named file
        # TODO maybe add check if the folder contains __init__.py

        module = importlib.import_module('.' + m + 'service', package='nnk.modules.' + m)

        assert hasattr(module,  m.capitalize() + 'Service')
        service = getattr(module, m.capitalize() + 'Service')
        # TODO maybe check whether the module starts properly
        # instance_queue = mp.Queue()
        # instance = service(self._sb.get_queue(), instance_queue)
        # process = mp.Process(target=instance.start, daemon=True)
        # process.start()
        #
        # # FIXME new modules should probably register by themselves with broker
        # self._sb.add_service(m, instance_queue)
        # # TODO replace state with string constants
        # self._moduleRegistry[m] = {'process': process, 'state': 'loaded', 'queue': instance_queue}
        #
        # lg.debug('started service: %s', m)
