from collections import namedtuple
from pathlib import Path

# Dataset and results root directory
_DATASET_ROOT = Path(__file__).parent / '../data'
RESULTS_ROOT = Path(__file__).parent / '../results'
RESULTS_ROOT.mkdir(exist_ok=True)

Dataset = namedtuple('Dataset', ['name', 'root', 'src', 'bug_repo', 'results'])

# Source codes and bug repositories
aspectj = Dataset(
    'aspectj',
    _DATASET_ROOT / 'AspectJ',
    _DATASET_ROOT / 'AspectJ/org.aspectj-bug433351',
    _DATASET_ROOT / 'AspectJ/AspectJ.txt',
    RESULTS_ROOT / 'AspectJ'
)

birt = Dataset(
    'birt',
    _DATASET_ROOT / 'Birt',
    _DATASET_ROOT / 'Birt/birt-20140211-1400',
    _DATASET_ROOT / 'Birt/Birt.txt',
    RESULTS_ROOT / 'Birt'
)

eclipse = Dataset(
    'eclipse',
    _DATASET_ROOT / 'Eclipse_Platform_UI',
    _DATASET_ROOT / 'Eclipse_Platform_UI/eclipse.platform.ui-johna-402445',
    _DATASET_ROOT / 'Eclipse_Platform_UI/Eclipse_Platform_UI.txt',
    RESULTS_ROOT / 'Eclipse_Platform_UI'
)

swt = Dataset(
    'swt',
    _DATASET_ROOT / 'SWT',
    _DATASET_ROOT / 'SWT/eclipse.platform.swt-xulrunner-31',
    _DATASET_ROOT / 'SWT/SWT.txt',
    RESULTS_ROOT / 'SWT'
)

tomcat = Dataset(
    'tomcat',
    _DATASET_ROOT / 'Tomcat',
    _DATASET_ROOT / 'Tomcat/tomcat-7.0.51',
    _DATASET_ROOT / 'Tomcat/Tomcat.txt',
    RESULTS_ROOT / 'Tomcat'
)

# Current dataset in use. (change this name to change the dataset)
DATASET = aspectj

if __name__ == '__main__':
    print(DATASET.name, DATASET.root, DATASET.src, DATASET.bug_repo, DATASET.results)
