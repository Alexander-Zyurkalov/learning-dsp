#!/usr/bin/env wolframscript

(* Mathematica Source File *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-08-11 *)

ts = 1/1000;
f = 10;
numberOfSamples = 100;
x = Table[Sin[2 Pi f n ts],  {n, 0, numberOfSamples - 1}];
xDecimated = Downsample[x, 2];

xShifted = RotateLeft[x, 1];
xShiftedAndDecimated = Downsample[xShifted, 2];
xDecimatedAndShifted = RotateLeft[xDecimated, 1];

GraphicsColumn[{
  Show[
    DiscretePlot[x[[n + 1]], {n, 0, numberOfSamples - 1}, PlotStyle -> Red],
    DiscretePlot[xShifted[[n + 1]], {n, 0, numberOfSamples - 1}, PlotStyle -> Green],
    PlotRange->{{0, numberOfSamples}, {-1, 1}}
  ],
  Show[
    DiscretePlot[xDecimated[[n + 1]], {n, 0, numberOfSamples - 1}, PlotStyle -> Red],
    DiscretePlot[xShiftedAndDecimated[[n + 1]], {n, 0, numberOfSamples - 1}, PlotStyle -> Green],
    DiscretePlot[xDecimatedAndShifted[[n + 1]], {n, 0, numberOfSamples - 1}, PlotStyle -> Blue],
    PlotRange->{{0, numberOfSamples}, {-1, 1}}
  ]
}]