from valexa.examples.test_feinberg_uncertainty import test_feinberg_uncertainty
from valexa.examples.test_feinberg_coli import test_feinberg_coli
from valexa.examples.test_sfstp import test_sfstp
from valexa.examples.test_intern_dataset import test_intern_dataset
from valexa.examples.test_feinberg_labostat import test_feinberg_labostat
from valexa.examples.test_inra_pyrene import test_inra_pyrene


def valexa_validate():

    test_feinberg_labostat()
    test_feinberg_uncertainty()
    test_feinberg_coli()
    test_feinberg_labostat()
    test_sfstp()
    test_inra_pyrene()
    test_intern_dataset()

    return True
