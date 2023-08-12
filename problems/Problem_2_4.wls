#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-12 *)
tf = 1/4000;
x = Table[ Cos[2 Pi 500 n tf + Pi/7], {n, 0, 100}];
DiscretePlot[x[[n]], {n, 1, Length[x]}]
