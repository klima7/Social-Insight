import pkgutil
import itertools
import traceback

_preprocessors = {}


# Dekorator służący do oznaczania funkcji dokonujących preprocessingu - wydobywania danych z zipa.
# Dane zwrócone przez udekorowaną funkcję są przypisywane do zmiennej o nazwie podanej w parametrze.
def preprocessor(*names):
    def decorator(fun):
        _preprocessors[names] = fun
    return decorator


def preprocess(zip_file):
    folders = get_structure(zip_file)

    preprocess_result = {}
    for names, fun in _preprocessors.items():
        try:
            result = fun(zip_file, folders)
        except Exception:
            result = ()
            print(f'-------------------- Exception in preprocessor -----------------------')
            traceback.print_exc()
        values = result if isinstance(result, tuple) else [result]
        for name, value in itertools.zip_longest(names, values):
            preprocess_result[name] = value
    return preprocess_result


def get_structure(zip_file):
    folders = {}
    for i in zip_file.namelist():
        entry = i.split('/')
        last = entry[-1]
        outer = folders
        for j in entry:
            if j != '':
                if j != last and j not in outer:
                    outer[j] = {}
                if j == last:
                    if '__files' not in outer:
                        outer['__files'] = []
                    outer['__files'].append((j, i))
                if j != last:
                    outer = outer[j]
    return folders


def fb_decode(text):
    return text.encode('latin1').decode('utf8')


def import_preprocessors():
    modules = [name for _, name, _ in pkgutil.iter_modules([f'analytics/preprocess'])]
    for module in modules:
        __import__(f'analytics.preprocess.{module}', fromlist=[f'analytics.preprocess'])


import_preprocessors()
