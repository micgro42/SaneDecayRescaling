from sanedecayrescaling import extract_decays
from pytest import fixture
import numpy

@fixture  # Registering this function as a fixture.
def relative_tolerance():
    return 1e-10

# D*+
def test_normal_percent_one_line_no_spaces():
    lines = "D0 pi+                                  (67.7+-0.5)%                       39\n"
    daughters, branching_fraction, branching_fraction_error = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["D0", "pi+"]
    assert branching_fraction == 0.677
    assert branching_fraction_error == 0.005


# D*+
def test_normal_percent_one_line_some_spaces_1():
    lines = "D+ gamma                                ( 1.6+-0.4)%                      136\n"
    daughters, branching_fraction, branching_fraction_error = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["D+", "gamma"]
    assert branching_fraction == 0.016
    assert branching_fraction_error == 0.004


# D+
def test_normal_percent_one_line_some_spaces_2():
    lines = "phi pi+ pi0                              ( 2.3 +-1.0       )%             619\n"
    daughters, branching_fraction, branching_fraction_error = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["phi", "pi+", "pi0"]
    assert branching_fraction == 0.023
    assert branching_fraction_error == 0.01


# D+
def test_normal_E3_one_line_some_spaces(relative_tolerance):
    lines = "pi0 e+ nu(e)                             ( 4.05+-0.18      )E-3           930"
    daughters, branching_fraction, branching_fraction_error = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["pi0", "e+", "nu(e)"]
    assert branching_fraction == 0.00405
    #assert branching_fraction_error == 0.00018
    rtol = 16
    numpy.testing.assert_allclose(branching_fraction_error, 0.00018, relative_tolerance)
    numpy.testing.assert_almost_equal(branching_fraction_error, 0.00018, rtol)
    numpy.testing.assert_approx_equal(branching_fraction_error, 0.00018, rtol)
