from sanedecayrescaling.extract_decays import make_single_line_snippets
from sanedecayrescaling.utility import *

def test_three_lines_break_both_columns_no_mini():
    line1 = "......Dbar(2)*(2460)0 lepton+ nu(l\      (  1.01 +-0.24        )\  S=2.0 2065\n"
    line2 = "epton)   x  B(Dbar(2)*0 --> D*- pi\     E-3\n"
    line3 = "+)\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1+line2+line3)
    assert column1 == '......Dbar(2)*(2460)0 lepton+ nu(lepton) x B(Dbar(2)*0 --> D*- pi+)'
    assert column2 == '(  1.01 +-0.24        )E-3'
    assert column3 == 'S=2.0 2065'
    assert column_mini == ''


def test_three_lines_break_first_columns_three_line_mini():
    line1 = "X(3872)+ K0   x  B(X(3872)+ --> J/\ [v\ <   6.1          E-6      CL=90%   --\n"
    line2 = "psi(1S) pi+ pi0)                    vv\\\n"
    line3 = "                                    v]"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
    assert column1 == 'X(3872)+ K0 x B(X(3872)+ --> J/psi(1S) pi+ pi0)'
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

def test_one_line_only_no_mini():
    line1 = "D+ gamma                                ( 1.6+-0.4)%                      136\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1)
    assert column1 == 'D+ gamma'
    assert column2 == '( 1.6+-0.4)%'
    assert column3 == '136'
    assert column_mini == ''

# B0
def test_three_lines_only_three_mini():
    line1 = "lepton+ nu(lepton) anything         [q\  ( 10.33+- 0.28       )%           --\n"
    line2 = "                                    qq\\\n"
    line3 = "                                    q]\n"
    try:
        column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
    except ParseError as e:
        print e.msg
        print e.line
        raise
    assert column1 == 'lepton+ nu(lepton) anything'
    assert column2 == '( 10.33+- 0.28       )%'
    assert column3 == '--'
    assert column_mini == '[qqqq]'

#B0
def test_two_lines_only_second_column():
    line1 = "...Dbar0 pi- lepton+ nu(lepton)          (  4.3 +- 0.6        )E\        2308\n"
    line2 = "                                        -3"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2)
    assert column1 == '...Dbar0 pi- lepton+ nu(lepton)'
    assert column2 == '(  4.3 +- 0.6        )E-3'
    assert column3 == '2308'
    assert column_mini == ''

# B+
def test_three_lines_all_first_column():
    line1 = "...Dbar(2)*(2462)0 pi+  x B(Dbar(2\     <   1.7          E-4      CL=90%   --\n"
    line2 = ")*0 --> Dbar0 pi- pi+ (nonresonant\\\n"
    line3 = "))\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
    assert column1 == '...Dbar(2)*(2462)0 pi+ x B(Dbar(2)*0 --> Dbar0 pi- pi+ (nonresonant))'
    assert column2 == '<   1.7          E-4'
    assert column3 == 'CL=90%   --'
    assert column_mini == ''

# B+
def test_one_line_single_letter_in_mini():
    line1 = "D- e+ mu+                        L      <   1.8          E-6      CL=90% 2307\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1)
    assert column1 == 'D- e+ mu+'
    assert column2 == '<   1.8          E-6'
    assert column3 == 'CL=90% 2307'
    assert column_mini == 'L'

# B+
def test_two_lines_two_letters_in_mini():
    line1 = "Lambdabar0 e+                    L\     <   8            E-8      CL=90%   --\n"
    line2 = "                                 ,B"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2)
    assert column1 == 'Lambdabar0 e+'
    assert column2 == '<   8            E-8'
    assert column3 == 'CL=90%   --'
    assert column_mini == 'L B'

#B+
def test_3_lines_1letter_4q_in_mini():
    line1 = "K*(892)+ lepton+ lepton-         B1 [q\  (  1.29 +-0.21        )\        2564\n"
    line2 = "                                    qq\\ E-6\n"
    line3 = "                                    q]\n"
    column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
    assert column1 == 'K*(892)+ lepton+ lepton-'
    assert column2 == '(  1.29 +-0.21        )E-6'
    assert column3 == '2564'
    assert column_mini == 'B1 [qqqq]'


#B+
# currently the following cases are skipped in the code, therefore they are not
# to be tested
# def test_3_lines_square_bracket_first_column_4s_in_mini():
#     line1 = "[ K- pi+ ](D) K+                    [s\ <   2.8          E-7      CL=90%   --\n"
#     line2 = "                                    ss\\\n"
#     line3 = "                                    s]\n"
#     column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
#     assert column1 == ''
#     assert column2 == '<   2.8          E-7'
#     assert column3 == 'CL=90%   --'
#     assert column_mini == ''
# 
# 
# def test_3_lines_square_bracket_first_column_no_mini():
#     line1 = "[ K+ pi- ](D) pi+                        (  2.0  +-0.4         )\          --\n"
#     line2 = "                                        E-4\n"
#     column1, column2, column3, column_mini = make_single_line_snippets(line1 + line2 + line3)
#     assert column1 == ''
#     assert column2 == '(  2.0  +-0.4         )E-4'
#     assert column3 == '--'
#     assert column_mini == ''
