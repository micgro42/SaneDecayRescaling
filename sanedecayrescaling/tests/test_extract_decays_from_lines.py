from sanedecayrescaling import extract_decays
from pytest import fixture
import numpy

@fixture  # Registering this function as a fixture.
def relative_tolerance():
    return 1e-10

# D*+
def test_normal_percent_one_line_no_spaces():
    lines = "D0 pi+                                  (67.7+-0.5)%                       39\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["D0", "pi+"]
    assert branching_fraction == 0.677
    assert branching_fraction_error_plus == 0.005
    assert branching_fraction_error_minus == 0.005


# D*+
def test_normal_percent_one_line_some_spaces_1():
    lines = "D+ gamma                                ( 1.6+-0.4)%                      136\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["D+", "gamma"]
    assert branching_fraction == 0.016
    assert branching_fraction_error_plus == 0.004
    assert branching_fraction_error_minus == 0.004


# D+
def test_normal_percent_one_line_some_spaces_2():
    lines = "phi pi+ pi0                              ( 2.3 +-1.0       )%             619\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["phi", "pi+", "pi0"]
    assert branching_fraction == 0.023
    assert branching_fraction_error_plus == 0.01
    assert branching_fraction_error_minus == 0.01


# D+
def test_normal_E3_one_line_some_spaces(relative_tolerance):
    lines = "pi0 e+ nu(e)                             ( 4.05+-0.18      )E-3           930"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(lines)
    assert daughters == ["pi0", "e+", "nu(e)"]
    assert branching_fraction == 0.00405
    #assert branching_fraction_error == 0.00018
    numpy.testing.assert_allclose(branching_fraction_error_plus, 0.00018, relative_tolerance)
    numpy.testing.assert_allclose(branching_fraction_error_minus, 0.00018, relative_tolerance)

# B0
def test_limit():
    line1 = "D+ X                                    <   3.9         %         CL=90%   --\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(line1)
    assert daughters == ["D+", "X"]
    assert branching_fraction == 0.039
    assert branching_fraction_error_plus == 0.00
    assert branching_fraction_error_minus == 0.00

# B0
def test_separate_errors(relative_tolerance):
    line1 = "D(s)+ X                                  ( 10.3 +  2.1  - 1.8 )%           --\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(line1)
    assert daughters == ["D(s)+", "X"]
    numpy.testing.assert_allclose(branching_fraction, 0.103, relative_tolerance)
    assert branching_fraction_error_plus == 0.021
    numpy.testing.assert_allclose(branching_fraction_error_minus, 0.018, relative_tolerance)

# B+
def test_single_letter_in_mini():
    line1 = "D- e+ mu+                        L      <   1.8          E-6      CL=90% 2307\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(line1)
    assert daughters == ["D-", "e+","mu+"]
    assert branching_fraction == 0.0000018
    assert branching_fraction_error_plus == 0.00
    assert branching_fraction_error_minus == 0.00

# invented
def test_not_seen():
    line1 = "K- pi0                                  not seen                        381\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(line1)
    assert daughters == ["K-", "pi0"]
    assert branching_fraction == 0.0
    assert branching_fraction_error_plus == 0.00
    assert branching_fraction_error_minus == 0.00

# D+
def test_remove_dots(relative_tolerance):
    line1 = "...rho0 pi+                              ( 8.1 +-1.5       )E-4           767\n"
    daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decays.extract_decay_from_lines(line1)
    assert daughters == ["rho0", "pi+"]
    assert branching_fraction == 0.00081
    numpy.testing.assert_allclose(branching_fraction_error_plus, 0.00015, relative_tolerance)
    numpy.testing.assert_allclose(branching_fraction_error_minus, 0.00015, relative_tolerance)

