Manipulate[
  Module[{w, T, x, y, transferFunction},
    w = 2 Pi f;
    T = 1/fs;
    x[n_] := Exp[I w n T];
    transferFunction[w_, a0_, a1_, d_] := a0 + a1 Exp[-I w d];
    y[n_] := x[n] * transferFunction[w, a0, a1, delay];


    magnitude = Abs[transferFunction[w, a0, a1, delay]];
    phase = Arg[transferFunction[w, a0, a1, delay]];

    GraphicsRow[{

      DiscretePlot[Im[x[n]], {n, 0, samples},
        PlotRange -> {{0, samples}, {-1.5, 1.5}}],

      DiscretePlot[Im[y[n]], {n, 0, samples},
        PlotRange -> {{0, samples}, {-1.5, 1.5}}],
      Show[
        PolarPlot[magnitude, {t, 0, 2 Pi}],

        Graphics[ {Red, Thickness[0.01],
          Line[{  {0, 0}, { magnitude* Cos[phase],
            magnitude * Sin[phase ]}  }] }  ],
        PlotRange -> {{-1.5, 1.5}, {-1.5, 1.5}},
        Frame -> True,
        FrameLabel -> {"Re", "Im"},
        AspectRatio -> 1,
        ImageSize -> Medium
      ]
    }, ImageSize -> 1000]
  ],
  {{fs, 400}, 100, 1000, 100},
  {{f, 10}, 1, 400, 1},
  {{samples, 1000}, 100, 2000, 100},
  {{a0, 0.5}, 0, 1, 0.1},
  {{a1, 0.5}, 0, 1, 0.1},
  {{delay, 0}, 0, 5, 1}
]