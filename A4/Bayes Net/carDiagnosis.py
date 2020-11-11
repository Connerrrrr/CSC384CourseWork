from bnetbase import *

al = Variable("Alternator", ['okay', 'faulty'])
F1 = Factor("P(al)", [al])
F1.add_values(
    [['okay', 0.997],
     ['faulty', 0.003]])

cs = Variable("Charging system",  ['okay', 'faulty'])
F2 = Factor("P(cs|al)", [cs, al])
F2.add_values(
    [['okay', 'okay', 0.5],
     ['okay', 'faulty', 0],
     ['faulty', 'okay', 0.5],
     ['faulty', 'faulty', 1]])

ba = Variable("Battery age", ['new', 'old', 'very_old'])
F3 = Factor("P(ba)", [ba])
F3.add_values(
    [['new', 0.4], 
     ['old', 0.4], 
     ['very_old', 0.2]])

bv = Variable("Battery voltage", ['strong', 'weak', 'dead'])
F4 = Factor("P(bv|cs,ba)", [bv, cs, ba])
F4.add_values(
    [['strong', 'okay', 'new', 0.95],
     ['weak', 'okay', 'new', 0.04],
     ['dead', 'okay', 'new', 0.01],
     ['strong', 'okay', 'old', 0.8],
     ['weak', 'okay', 'old', 0.15],
     ['dead', 'okay', 'old', 0.05],
     ['strong', 'okay', 'very_old', 0.6],
     ['weak', 'okay', 'very_old', 0.3],
     ['dead', 'okay', 'very_old', 0.1],
     ['strong', 'faulty', 'new', 0.008],
     ['weak', 'faulty', 'new', 0.3],
     ['dead', 'faulty', 'new', 0.692],
     ['strong', 'faulty', 'old', 0.004],
     ['weak', 'faulty', 'old', 0.2],
     ['dead', 'faulty', 'old', 0.796],
     ['strong', 'faulty', 'very_old', 0.002],
     ['weak', 'faulty', 'very_old', 0.1],
     ['dead', 'faulty', 'very_old', 0.898]])


mf = Variable("Main fuse", ['okay', 'blown'])
F5 = Factor("P(mf)", [mf])
F5.add_values(
    [['okay', 0.99],
    ['blown', 0.01]])

ds = Variable("Distributer", ['okay', 'faulty'])
F6 = Factor("P(ds)", [ds])
F6.add_values(
    [['okay', 0.99],
     ['faulty', 0.00999999]])

pv = Variable("Voltage at plug", ['strong', 'weak', 'none'])
F7 = Factor("P(pv|mf,ds,bv)", [pv, mf, ds, bv])
F7.add_values([
     ['strong', 'okay', 'okay', 'strong', 0.9],
     ['weak', 'okay', 'okay', 'strong', 0.05],
     ['none', 'okay', 'okay', 'strong', 0.05],

     ['strong', 'okay', 'okay', 'weak', 0.0],
     ['weak', 'okay', 'okay', 'weak', 0.9],
     ['none', 'okay', 'okay', 'weak', 0.1], 

     ['strong', 'okay', 'okay', 'dead', 0],
     ['weak', 'okay', 'okay', 'dead', 0],
     ['none', 'okay', 'okay', 'dead', 1], 

     ['strong', 'okay', 'faulty', 'strong', 0.1],
     ['weak', 'okay', 'faulty', 'strong', 0.1],
     ['none', 'okay', 'faulty', 'strong', 0.8],

     ['strong', 'okay', 'faulty', 'weak', 0],
     ['weak', 'okay', 'faulty', 'weak', 0.1],
     ['none', 'okay', 'faulty', 'weak', 0.9], 

     ['strong', 'okay', 'faulty', 'dead', 0],
     ['weak', 'okay', 'faulty', 'dead', 0],
     ['none', 'okay', 'faulty', 'dead', 1], 

     ['strong', 'blown', 'okay', 'strong', 0],
     ['weak', 'blown', 'okay', 'strong', 0],
     ['none', 'blown', 'okay', 'strong', 1],

     ['strong', 'blown', 'okay', 'weak', 0],
     ['weak', 'blown', 'okay', 'weak', 0],
     ['none', 'blown', 'okay', 'weak', 1],

     ['strong', 'blown', 'okay', 'dead', 0],
     ['weak', 'blown', 'okay', 'dead', 0],
     ['none', 'blown', 'okay', 'dead', 1],

     ['strong', 'blown', 'faulty', 'strong', 0],
     ['weak', 'blown', 'faulty', 'strong', 0],
     ['none', 'blown', 'faulty', 'strong', 1],

     ['strong', 'blown', 'faulty', 'weak', 0],
     ['weak', 'blown', 'faulty', 'weak', 0],
     ['none', 'blown', 'faulty', 'weak', 1],

     ['strong', 'blown', 'faulty', 'dead', 0],
     ['weak', 'blown', 'faulty', 'dead', 0],
     ['none', 'blown', 'faulty', 'dead', 1]])

sm = Variable("Starter Motor", ['okay', 'faulty'])
F8 = Factor("P(sm)", [sm])
F8.add_values([
    ['okay', 0.995],
    ['faulty', 0.004999995]])

ss = Variable("Starter system", ['okay', 'faulty'])
F9 = Factor("P(ss|mf, sm, bv)", [ss, mf, sm, bv])
F9.add_values([
    ['okay', 'okay', 'okay', 'strong', 0.98], 
    ['faulty', 'okay', 'okay', 'strong', 0.02], 
    ['okay', 'okay', 'okay', 'weak', 0.9], 
    ['faulty', 'okay', 'okay', 'weak', 0.1], 
    ['okay', 'okay', 'okay', 'dead', 0.1], 
    ['faulty', 'okay', 'okay', 'dead', 0.9], 
    ['okay', 'okay', 'faulty', 'strong', 0.02], 
    ['faulty', 'okay', 'faulty', 'strong', 0.98], 
    ['okay', 'okay', 'faulty', 'weak', 0.01], 
    ['faulty', 'okay', 'faulty', 'weak', 0.99], 
    ['okay', 'okay', 'faulty', 'dead', 0.005], 
    ['faulty', 'okay', 'faulty', 'dead', 0.995], 
    ['okay', 'blown', 'okay', 'strong', 0], 
    ['faulty', 'blown', 'okay', 'strong', 1], 
    ['okay', 'blown', 'okay', 'weak', 0], 
    ['faulty', 'blown', 'okay', 'weak', 1], 
    ['okay', 'blown', 'okay', 'dead', 0], 
    ['faulty', 'blown', 'okay', 'dead', 1], 
    ['okay', 'blown', 'faulty', 'strong', 0], 
    ['faulty', 'blown', 'faulty', 'strong', 1], 
    ['okay', 'blown', 'faulty', 'weak', 0], 
    ['faulty', 'blown', 'faulty', 'weak', 1], 
    ['okay', 'blown', 'faulty', 'dead', 0], 
    ['faulty', 'blown', 'faulty', 'dead', 1]])

hl = Variable("Headlights", ['bright', 'dim', 'off'])
F10 = Factor("P(hl|bv)", [hl, bv])
F10.add_values([
		 ['bright', 'strong', 0.94],
		 ['dim',    'strong', 0.01],
		 ['off',    'strong', 0.05],

		 ['bright', 'weak', 0],
		 ['dim',    'weak', 0.95],
		 ['off',    'weak',  0.05],

		 ['bright',  'dead', 0],
		 ['dim',     'dead', 0],
		 ['off',     'dead', 1]])

sp = Variable("Spark plugs", ['okay', 'too_wide', 'fouled'])
F11 = Factor("P(sp)", [sp])
F11.add_values([
    ['okay', 0.7],
    ['too_wide', 0.1],
    ['fouled', 0.2]])

sq = Variable("Spark quality", ['good', 'bad', 'very_bad'])
F12 = Factor("P(sq|sp,pv)", [sq, sp, pv])
F12.add_values([
		['good',     'okay', 'strong', 1],
        ['bad' ,     'okay', 'strong', 0],
        ['very_bad', 'okay', 'strong', 0], 
    	['good',     'okay', 'weak', 0],
        ['bad' ,     'okay', 'weak', 1],
        ['very_bad', 'okay', 'weak', 0],             
    	['good',     'okay', 'none', 0],
        ['bad' ,     'okay', 'none', 0],
        ['very_bad', 'okay', 'none', 1],

		['good',     'too_wide', 'strong', 0],
        ['bad' ,     'too_wide', 'strong', 1],
        ['very_bad', 'too_wide', 'strong', 0], 
    	['good',     'too_wide', 'weak', 0],
        ['bad' ,     'too_wide', 'weak', 0],
        ['very_bad', 'too_wide', 'weak', 1],             
    	['good',     'too_wide', 'none', 0],
        ['bad' ,     'too_wide', 'none', 0],
        ['very_bad', 'too_wide', 'none', 1],

		['good',     'fouled', 'strong', 0],
        ['bad' ,     'fouled', 'strong', 1],
        ['very_bad', 'fouled', 'strong', 0], 
    	['good',     'fouled', 'weak', 0],
        ['bad' ,     'fouled', 'weak', 0],
        ['very_bad', 'fouled', 'weak', 1],             
    	['good',     'fouled', 'none', 0],
        ['bad' ,     'fouled', 'none', 0],
        ['very_bad', 'fouled', 'none', 1]])

cc = Variable("Car cranks", ['true', 'false'])
F13 = Factor("P(cc|ss)", [cc, ss])
F13.add_values([
    ['true',  'okay', 0.8],
    ['false', 'okay', 0.2],
    ['true',  'faulty', 0.05], 
    ['false', 'faulty', 0.95]])

tm = Variable("Spark timing", ['good', 'bad', 'very_bad'])
F14 = Factor("P(tm|ds)", [tm, ds])
F14.add_values([
    ['good',     'okay',  0.9],
    ['bad',      'okay', 0.09],
    ['very_bad', 'okay', 0.01],
    ['good',     'faulty', 0.2],
    ['bad',      'faulty', 0.3],
    ['very_bad', 'faulty', 0.5]])

fs = Variable("Fuel system", ['okay', 'faulty'])
F15 = Factor("P(fs)", [fs])
F15.add_values([
    ['okay',   0.9],
    ['faulty', 0.1]])

af = Variable("Air filter", ['clean', 'dirty'])
F16 = Factor("P(af)", [af])
F16.add_values([
    ['clean', 0.9],
    ['dirty', 0.1]])

asys = Variable("Air system", ['okay', 'faulty'])
F17 = Factor("P(asys|af)", [asys, af])
F17.add_values([
    ['okay',   'clean', 0.9],
    ['faulty', 'clean', 0.1],
    ['okay',   'dirty', 0.3],
    ['faulty', 'dirty', 0.7]])

st = Variable("Car starts", ['true', 'false'])
F18 = Factor("P(st|cc, fs, sq, asys, tm)", [st, cc, fs, sq, asys, tm])
F18.add_values([
    ['true', 'true', 'okay', 'good', 'okay', 'good', 0.99], 
    ['false','true', 'okay', 'good', 'okay', 'good', 0.01],
    ['true', 'true', 'okay', 'good', 'okay', 'bad', 0.98],
    ['false','true', 'okay', 'good', 'okay', 'bad', 0.02],
    ['true', 'true', 'okay', 'good', 'okay', 'very_bad', 0.7], 
    ['false','true', 'okay', 'good', 'okay', 'very_bad', 0.3], 
    ['true', 'true', 'okay', 'good', 'faulty', 'good', 0.8], 
    ['false','true', 'okay', 'good', 'faulty', 'good', 0.2], 
    ['true', 'true', 'okay', 'good', 'faulty', 'bad', 0.75],
    ['false','true', 'okay', 'good', 'faulty', 'bad', 0.25],
    ['true', 'true', 'okay', 'good', 'faulty', 'very_bad', 0.6], 
    ['false','true', 'okay', 'good', 'faulty', 'very_bad', 0.4], 
    ['true', 'true', 'okay', 'bad', 'okay', 'good', 0.7], 
    ['false','true', 'okay', 'bad', 'okay', 'good', 0.3], 
    ['true', 'true', 'okay', 'bad', 'okay', 'bad', 0.65],
    ['false','true', 'okay', 'bad', 'okay', 'bad', 0.35],
    ['true', 'true', 'okay', 'bad', 'okay', 'very_bad', 0.5], 
    ['false','true', 'okay', 'bad', 'okay', 'very_bad', 0.5], 
    ['true', 'true', 'okay', 'bad', 'faulty', 'good', 0.6], 
    ['false','true', 'okay', 'bad', 'faulty', 'good', 0.4], 
    ['true', 'true', 'okay', 'bad', 'faulty', 'bad', 0.5], 
    ['false','true', 'okay', 'bad', 'faulty', 'bad', 0.5], 
    ['true', 'true', 'okay', 'bad', 'faulty', 'very_bad', 0.4], 
    ['false','true', 'okay', 'bad', 'faulty', 'very_bad', 0.6], 
    ['true', 'true', 'okay', 'very_bad', 'okay', 'good', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'good', 1], 
    ['true', 'true', 'okay', 'very_bad', 'okay', 'bad', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'bad', 1], 
    ['true', 'true', 'okay', 'very_bad', 'okay', 'very_bad', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'very_bad', 1], 
    ['true', 'true', 'okay', 'very_bad', 'faulty', 'good', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'good', 1], 
    ['true', 'true', 'okay', 'very_bad', 'faulty', 'bad', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'bad', 1], 
    ['true', 'true', 'okay', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'very_bad', 1], 
    ['true', 'true', 'faulty', 'good', 'okay', 'good', 0.1], 
    ['false','true', 'faulty', 'good', 'okay', 'good', 0.9], 
    ['true', 'true', 'faulty', 'good', 'okay', 'bad', 0.05],
    ['false','true', 'faulty', 'good', 'okay', 'bad', 0.95],
    ['true', 'true', 'faulty', 'good', 'okay', 'very_bad', 0.02],
    ['false','true', 'faulty', 'good', 'okay', 'very_bad', 0.98],
    ['true', 'true', 'faulty', 'good', 'faulty', 'good', 0.05],
    ['false','true', 'faulty', 'good', 'faulty', 'good', 0.95],
    ['true', 'true', 'faulty', 'good', 'faulty', 'bad', 0.02],
    ['false','true', 'faulty', 'good', 'faulty', 'bad', 0.98],
    ['true', 'true', 'faulty', 'good', 'faulty', 'very_bad', 0.01],
    ['false','true', 'faulty', 'good', 'faulty', 'very_bad', 0.99],
    ['true', 'true', 'faulty', 'bad', 'okay', 'good', 0.05],
    ['false','true', 'faulty', 'bad', 'okay', 'good', 0.95],
    ['true', 'true', 'faulty', 'bad', 'okay', 'bad', 0.02],
    ['false','true', 'faulty', 'bad', 'okay', 'bad', 0.98],
    ['true', 'true', 'faulty', 'bad', 'okay', 'very_bad', 0.01],
    ['false','true', 'faulty', 'bad', 'okay', 'very_bad', 0.99],
    ['true', 'true', 'faulty', 'bad', 'faulty', 'good', 0.02],
    ['false','true', 'faulty', 'bad', 'faulty', 'good', 0.98],
    ['true', 'true', 'faulty', 'bad', 'faulty', 'bad', 0.01],
    ['false','true', 'faulty', 'bad', 'faulty', 'bad', 0.99],
    ['true', 'true', 'faulty', 'bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'faulty', 'bad', 'faulty', 'very_bad', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'okay', 'good', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'good', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'okay', 'bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'bad', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'okay', 'very_bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'very_bad', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'good', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'good', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'bad', 1], 
    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'okay', 'good', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'good', 1], 
    ['true', 'false', 'okay', 'good', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'bad', 1], 
    ['true', 'false', 'okay', 'good', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'very_bad', 1], 
    ['true', 'false', 'okay', 'good', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'good', 1], 
    ['true', 'false', 'okay', 'good', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'bad', 1], 
    ['true', 'false', 'okay', 'good', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'okay', 'bad', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'good', 1], 
    ['true', 'false', 'okay', 'bad', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'bad', 1], 
    ['true', 'false', 'okay', 'bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'very_bad', 1], 
    ['true', 'false', 'okay', 'bad', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'good', 1], 
    ['true', 'false', 'okay', 'bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'bad', 1], 
    ['true', 'false', 'okay', 'bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'okay', 'very_bad', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'good', 1], 
    ['true', 'false', 'okay', 'very_bad', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'bad', 1], 
    ['true', 'false', 'okay', 'very_bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'very_bad', 1], 
    ['true', 'false', 'okay', 'very_bad', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'good', 1], 
    ['true', 'false', 'okay', 'very_bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'bad', 1], 
    ['true', 'false', 'okay', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'good', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'good', 1], 
    ['true', 'false', 'faulty', 'good', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'bad', 1], 
    ['true', 'false', 'faulty', 'good', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'good', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'good', 1], 
    ['true', 'false', 'faulty', 'good', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'bad', 1], 
    ['true', 'false', 'faulty', 'good', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'bad', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'good', 1], 
    ['true', 'false', 'faulty', 'bad', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'bad', 1], 
    ['true', 'false', 'faulty', 'bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'bad', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'good', 1], 
    ['true', 'false', 'faulty', 'bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'bad', 1], 
    ['true', 'false', 'faulty', 'bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'good', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'bad', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'very_bad', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'good', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'bad', 1], 
    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'very_bad', 1]])

car = BN('Car Diagnosis', 
         [al, cs, ba, bv, mf, ds, pv, sm, ss, hl,   sp,  sq,  cc,  tm,  fs,  af, asys, st], 
         [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18])

if __name__ == '__main__':

    for v in [al, cs, ba, bv, mf, ds, pv, sm, ss, hl,   sp,  sq,  cc,  tm,  fs,  af, asys, st]:
        print("Variable:", v.name)
        probs = VE(car, v, [])
        doms = v.domain()
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(v.name, doms[i], 100*probs[i]))
        print()

    v = al
    for t in [ba, bv, mf, ds, pv, sm, ss, hl,   sp,  sq,  cc,  tm,  fs,  af, asys, st]:
        print("Variable:", t.name)        
        probs = VE(car, v, [t, ba])
        probs1 = VE(car, v, [ba])
        print(probs1)
        print(probs)
        doms = v.domain()
        #for i in range(len(probs)):
        #    for j in range(len(probs)):
        #        print("P({0:} = {1:}|{0:} = {1:}) = {2:0.1f}".format(v.name, t.name, doms[i], 100*probs[i]))
        print()
