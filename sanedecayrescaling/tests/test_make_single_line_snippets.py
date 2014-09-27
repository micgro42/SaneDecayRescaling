from sanedecayrescaling.extract_decays import make_single_line_snippets

def test_three_lines_break_both_columns_no_mini():
    line1 = "......Dbar(2)*(2460)0 lepton+ nu(l\      (  1.01 +-0.24        )\  S=2.0 2065\n"
    line2 = "epton)   x  B(Dbar(2)*0 --> D*- pi\     E-3\n"
    line3 = "+)\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1+line2+line3)
    assert column1 == '......Dbar(2)*(2460)0 lepton+ nu(lepton)   x  B(Dbar(2)*0 --> D*- pi+)'
    assert column2 == ' (  1.01 +-0.24        )E-3'
    assert column3 == ' S=2.0 2065'
    assert column_mini == ''


def test_three_lines_break_first_columns_three_line_mini():
    line1 = "X(3872)+ K0   x  B(X(3872)+ --> J/\ [v\ <   6.1          E-6      CL=90%   --\n"
    line2 = "psi(1S) pi+ pi0)                    vv\\\n"
    line3 = "                                    v]"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
    assert column1 == 'X(3872)+ K0   x  B(X(3872)+ --> J/psi(1S) pi+ pi0)'
    assert column2 == '<   6.1          E-6'
    assert column3 == 'CL=90%   --'
    assert column_mini == '[vvvv]'


def test_two_lines_break_first_columns_two_line_mini():
    line1 = "pi+ mu+ mu-                         [v\ <   2.6        E-5        CL=90%  968\n"
    line2 = "                                    vv]\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2)
    assert column1 == 'pi+ mu+ mu-'
    assert column2 == '<   2.6        E-5'
    assert column3 == 'CL=90%  968'
    assert column_mini == '[vvv]'
