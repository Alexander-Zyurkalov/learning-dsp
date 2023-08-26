#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-26 *)
Manipulate[
    Module[{x, fs},
        fs = 160;

        x[t_] := Sin[2 Pi f t 1/fs];
        DiscretePlot[x[t], {t, 0, 100}]
    ],
    {{f, 10, "Frequency"}, {1, 5, 10, 100, 160, 170, 300, 330, 440}}
]