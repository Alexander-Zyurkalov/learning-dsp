#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-13 *)

f1 = 2000;
f2 = 100;


f[t_] := Cos[2 Pi f1 t] + Cos[2 Pi f2 t];

(* Sampling parameters *)
fs = 5000; (* Sampling frequency, should be at least 2 times the highest frequency in the signal for Nyquist criterion *)
Tmax = 1; (* Duration for which the signal is sampled *)
tValues = Range[0, Tmax, 1/fs]; (* Discrete time values *)

(* Sample the function *)
samples = f /@ tValues;

(* Perform FFT *)
fftValues = Fourier[samples, FourierParameters -> {-1, 1}];
(* Frequency axis for plotting *)
freqs = Range[0, fs, fs/Length[fftValues]];


freqs


