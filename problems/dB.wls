#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-29 *)

Manipulate[Module[{amplitude, phase},
        amplitude = 1;
        phase = 0;
        Show[
            Plot[amplitude*Sin[2*Pi*frequency*t + phase], {t, 0, 1}, PlotRange -> {-1, 1}],
            Plot[amplitude*Cos[2*Pi*frequency*t + phase], {t, 0, 1}, PlotRange -> {-1, 1}, PlotStyle -> Red]
        ]

    ],
    {frequency, 1, 60, 1}
]