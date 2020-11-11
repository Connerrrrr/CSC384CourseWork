##Three sample bayes nets are defined here. ##
from bnetbase import *

VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
F1 = Factor("F1", [VisitAsia])
F1.add_values([['visit', 0.01], ['no-visit', 0.99]])

Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
F2 = Factor("F2", [Smoking])
F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])

Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
F3 = Factor("F3", [Tuberculosis, VisitAsia])
F3.add_values([['present', 'visit', 0.05],
               ['present', 'no-visit', 0.01],
               ['absent', 'visit', 0.95],
               ['absent', 'no-visit', 0.99]])

Cancer = Variable('Lung Cancer', ['present', 'absent'])
F4 = Factor("F4", [Cancer, Smoking])
F4.add_values([['present', 'smoker', 0.10],
               ['present', 'non-smoker', 0.01],
               ['absent', 'smoker', 0.90],
               ['absent', 'non-smoker', 0.99]])

Bronchitis = Variable('Bronchitis', ['present', 'absent'])
F5 = Factor("F5", [Bronchitis, Smoking])
F5.add_values([['present', 'smoker', 0.60],
               ['present', 'non-smoker', 0.30],
               ['absent', 'smoker', 0.40],
               ['absent', 'non-smoker', 0.70]])

TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
F6.add_values([['true', 'present', 'present', 1.0],
               ['true', 'present', 'absent', 1.0],
               ['true', 'absent', 'present', 1.0],
               ['true', 'absent', 'absent', 0],
               ['false', 'present', 'present', 0],
               ['false', 'present', 'absent', 0],
               ['false', 'absent', 'present', 0],
               ['false', 'absent', 'absent', 1]])

Dyspnea = Variable('Dyspnea', ['present', 'absent'])
F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
F7.add_values([['present', 'true', 'present', 0.9],
               ['present', 'true', 'absent', 0.7],
               ['present', 'false', 'present', 0.8],
               ['present', 'false', 'absent', 0.1],
               ['absent', 'true', 'present', 0.1],
               ['absent', 'true', 'absent', 0.3],
               ['absent', 'false', 'present', 0.2],
               ['absent', 'false', 'absent', 0.9]])

Xray = Variable('XRay Result', ['abnormal', 'normal'])
F8 = Factor("F8", [Xray, TBorCA])
F8.add_values([['abnormal', 'true', 0.98],
               ['abnormal', 'false', 0.05],
               ['normal', 'true', 0.02],
               ['normal', 'false', 0.95]])

Asia = BN("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                   Bronchitis, TBorCA, Dyspnea, Xray],
          [F1, F2, F3, F4, F5, F6, F7, F8])

## E,B,S,w,G example from sample questions
E = Variable('E', ['e', '-e'])
B = Variable('B', ['b', '-b'])
S = Variable('S', ['s', '-s'])
G = Variable('G', ['g', '-g'])
W = Variable('W', ['w', '-w'])
FE = Factor('P(E)', [E])
FB = Factor('P(B)', [B])
FS = Factor('P(S|E,B)', [S, E, B])
FG = Factor('P(G|S)', [G, S])
FW = Factor('P(W|S)', [W, S])

FE.add_values([['e', 0.1], ['-e', 0.9]])
FB.add_values([['b', 0.1], ['-b', 0.9]])
FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8], ['s', '-e', '-b', 0],
               ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2], ['-s', '-e', '-b', 1]])
FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

Q3 = BN('SampleQ4', [E, B, S, G, W], [FE, FB, FS, FG, FW])

if __name__ == '__main__':
    ## NEW TESTS ##
    print("Multiply Factors Tests")
    print("Test 1 ....", end='')

    factor = multiply_factors([FE])
    values = (factor.get_value(['e']), factor.get_value(['-e']))
    if values[0] == 0.1 and values[1] == 0.9:
        print("passed.")
    else:
        print("failed.")
    print('P(e) = {} P(-e) = {}'.format(values[0], values[1]))

    print("Test 2 ....", end='')
    factor = multiply_factors([FE, FB])
    values = (factor.get_value(['e', 'b']), factor.get_value(['-e', 'b']), factor.get_value(['e', '-b']),
              factor.get_value(['-e', '-b']))
    if values[0] == FE.get_value(['e']) * FB.get_value(['b']) and values[1] == FE.get_value(['-e']) * FB.get_value(
            ['b']) and values[2] == FE.get_value(['e']) * FB.get_value(['-b']) and values[3] == FE.get_value(
            ['-e']) * FB.get_value(['-b']):
        print("passed.")
    else:
        print("failed.")
    print('P(e,b) = {} P(-e,b) = {} P(e,-b) = {} P(-e,-b) = {}'.format(values[0], values[1], values[2], values[3]))

    print("Test 3 ....", end='')
    factor = multiply_factors([FE, FS])
    values = (
    factor.get_value(['e', 's', 'b']), factor.get_value(['-e', 's', 'b']), factor.get_value(['e', '-s', '-b']),
    factor.get_value(['-e', 's', '-b']))
    if values[0] == FE.get_value(['e']) * FS.get_value(['s', 'e', 'b']) and values[1] == FE.get_value(
            ['-e']) * FS.get_value(['s', '-e', 'b']) and values[2] == FE.get_value(['e']) * FS.get_value(
            ['-s', 'e', '-b']) and values[3] == FE.get_value(['-e']) * FS.get_value(['s', '-e', '-b']):
        print("passed.")
    else:
        print("failed.")
    print('P(e,s,b) = {} P(-e,s,b) = {} P(e,-s,-b) = {} P(-e,s,-b) = {}'.format(values[0], values[1], values[2],
                                                                                values[3]))

    ##
    print("\n\nRestrict Factor Tests")
    print("Test 1 ....", end='')
    factor = restrict_factor(FE, E, 'e')
    value = factor.get_value_at_current_assignments()
    if value == 0.1:
        print("passed.")
    else:
        print("failed.")
    print('P(E=e) = {}'.format(value))

    print("Test 2 ....", end='')
    factor = restrict_factor(FG, S, 's')
    value = factor.get_value_at_current_assignments()
    if value == 0.5:
        print("passed.")
    else:
        print("failed.")
    print('P(G|S=s) = {}'.format(value))

    print("Test 3 ....", end='')
    factor = restrict_factor(FS, S, '-s')
    factor = restrict_factor(factor, E, '-e')
    factor = restrict_factor(factor, B, 'b')
    value = factor.get_value_at_current_assignments()
    if value == .2:
        print("passed.")
    else:
        print("failed.")
    print('P(S=-s|E=-e,B=b) = {}'.format(value))

    print("\n\nNormalize Tests")
    print("Test 1 ....", end='')
    normalized_nums = normalize([i for i in range(5)])
    norm_sum = sum(normalized_nums)
    if norm_sum == 1:
        print("passed.")
    else:
        print("failed.")
    print('{} when normalized to {} sum to {}'.format([i for i in range(5)], normalized_nums, norm_sum))

    print("Test 2 ....", end='')
    normalized_nums = normalize([i for i in range(0, -5, -1)])
    norm_sum = sum(normalized_nums)
    if norm_sum == 1:
        print("passed.")
    else:
        print("failed.")
    print('{} when normalized to {} sum to {}'.format([i for i in range(0, -5, -1)], normalized_nums, norm_sum))

    print("Test 3 ....", end='')
    normalized_nums = normalize([i for i in range(4, -5, -1)])
    norm_sum = sum(normalized_nums)
    if norm_sum == 0:
        print("passed.")
    else:
        print("failed.")
    print('{} when normalized to {} sum to {}'.format([i for i in range(4, -5, -1)], normalized_nums, norm_sum))

    # (a)
    print("\n\nTest 1 ....", end='')
    G.set_evidence('g')
    probs = VE(Q3, S, [G])
    if probs[0] == 1 and probs[1] == 0:
        print("passed.")
    else:
        print("failed.")

    print('P(s|g) = {} P(-s|g) = {}'.format(probs[0], probs[1]))

    # (b)
    print("\n\nTest 2 ....", end='')
    B.set_evidence('b')
    E.set_evidence('-e')
    probs = VE(Q3, W, [B, E])
    if abs(probs[0] - 0.68) < 0.0001 and abs(probs[1] - 0.32) < 0.0001:
        print("passed.")
    else:
        print("failed.")

    print('P(w|b,-e) = {} P(-w|b,-e) = {}'.format(probs[0], probs[1]))

    # (c)
    print("\n\nTest 3 ....", end='')
    S.set_evidence('s')
    probs1 = VE(Q3, G, [S])
    S.set_evidence('-s')
    probs2 = VE(Q3, G, [S])
    if probs1[0] == 0.5 and probs1[1] == 0.5 and probs2[0] == 0.0 and probs2[1] == 1.0:
        print("passed.")
    else:
        print("failed.")
    print('P(g|s) = {} P(-g|s) = {} P(g|-s) = {} P(-g|-s) = {}'.format(probs1[0], probs1[1], probs2[0], probs2[1]))

    # (d)
    print("\n\nTest 4 ....", end='')
    S.set_evidence('s')
    W.set_evidence('w')
    probs1 = VE(Q3, G, [S, W])
    S.set_evidence('s')
    W.set_evidence('-w')
    probs2 = VE(Q3, G, [S, W])
    if probs1[0] == 0.5 and probs1[1] == 0.5 and probs2[0] == 0.5 and probs2[1] == 0.5:
        print("passed.")
    else:
        print("failed.")
    print('P(g|s,w) = {} P(-g|s,w) = {} P(g|s,-w) = {} P(-g|s,-w) = {}'.format(probs1[0], probs1[1], probs2[0],
                                                                               probs2[1]))

    print("\n\nTest 5 ....", end='')
    S.set_evidence('-s')
    W.set_evidence('w')
    probs3 = VE(Q3, G, [S, W])
    S.set_evidence('-s')
    W.set_evidence('-w')
    probs4 = VE(Q3, G, [S, W])
    if probs3[0] == 0.0 and probs3[1] == 1.0 and probs4[0] == 0.0 and probs4[1] == 1.0:
        print("passed.")
    else:
        print("failed.")
    print('P(g|-s,w) = {} P(-g|-s,w) = {} P(g|-s,-w) = {} P(-g|-s,-w) = {}'.format(probs3[0], probs3[1], probs4[0],
                                                                                   probs4[1]))

    # (f)
    print("\n\nTest 6 ....", end='')
    W.set_evidence('w')
    probs1 = VE(Q3, G, [W])
    W.set_evidence('-w')
    probs2 = VE(Q3, G, [W])
    if abs(probs1[0] - 0.15265998457979954) < 0.0001 and abs(probs1[1] - 0.8473400154202004) < 0.0001 and abs(
            probs2[0] - 0.01336753983256819) < 0.0001 and abs(probs2[1] - 0.9866324601674318) < 0.0001:
        print("passed.")
    else:
        print("failed.")
    print('P(g|w) = {} P(-g|w) = {} P(g|-w) = {} P(-g|-w) = {}'.format(probs1[0], probs1[1], probs2[0], probs2[1]))

    # (h)
    print("\n\nTest 7 ....", end='')
    probs = VE(Q3, G, [])
    if abs(probs[0] - 0.04950000000000001) < .0001 and abs(probs[1] - 0.9505) < .0001:
        print("passed.")
    else:
        print("failed.")
    print('P(g) = {} P(-g) = {}'.format(probs[0], probs[1]))

    print("\n\nTest 8 ....", end='')
    probs = VE(Q3, E, [])
    if abs(probs[0] - 0.1) < 0.0001 and abs(probs[1] - 0.9) < 0.0001:
        print("passed.")
    else:
        print("failed.")
    print('P(e) = {} P(-e) = {}'.format(probs[0], probs[1]))
