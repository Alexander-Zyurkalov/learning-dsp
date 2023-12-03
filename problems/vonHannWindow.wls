#!/usr/bin/env wolframscript

dataLength = 100;
x = Table[RandomReal[], {dataLength}];

vonHann = Table[0.5 - 0.5 Cos[2 Pi n / (dataLength - 1)], {n, 1, dataLength}];

size = 400;
data = x * vonHann;
Column[
    {
        DiscretePlot[x[[i]], {i, 1, Length[x]}, PlotStyle -> Gray, ImageSize-> size ],
        DiscretePlot[vonHann[[i]], {i, 1, Length[vonHann]}, PlotStyle -> Gray, ImageSize-> size ],
        DiscretePlot[data[[i]], {i, 1, Length[data]}, PlotStyle -> Blue, ImageSize-> size ]
    }
]
