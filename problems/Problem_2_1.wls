#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-11 *)

Manipulate[
  Module[{start, minutes, degree, radians},
    minutes = step*numberOfSteps;

    degree = minutes*6 - 180;
    radians = degree*Pi/180;
    Show[
      PolarPlot[1, {theta, 0, 2 Pi}],
      Graphics[{
        Red,
        Line[{{0, 0}, {Cos[radians], Sin[radians]}}]
      }]
    ]
  ],
  {{step, 55}, 0, 60, 1},
  {{numberOfSteps, 0}, 0, 60, 1}
]

