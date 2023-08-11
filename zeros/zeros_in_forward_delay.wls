Manipulate[
 Module[{T, zero, zeroPoint, points, omega, distances, textPositions},
  T = 1/fs;
  H[z_, a0_, a1_] := a0 + a1 z^-1;
  zero = z /. First[Quiet[Solve[H[z, a0, a1] == 0, z], Solve::ratnz]];
  zeroPoint = {Re[zero], Im[zero]};
  omega = 2 Pi {f1, f2, f3}/fs; (* Convert to angular frequencies *)
  points = Table[{Cos[w], Sin[w]}, {w, omega}];
  distances = EuclideanDistance[zeroPoint, #] & /@ points;

  textPositions = Table[zeroPoint + 0.7 (p - zeroPoint), {p, points}];

  Graphics[{
    Circle[],
    PointSize[Large],
    Red, Point[zeroPoint],
    Blue, Point /@ points,
    Green, Line[{{Re[zero], Im[zero]}, #}] & /@ points,
    Gray, MapThread[Text[Style[NumberForm[#1, {4, 2}], 12], #2] &, {distances, textPositions}]
    },
   Axes -> True, PlotRange -> {{-1.5, 1.5}, {-1.5, 1.5}}
   ]
  ],
 {{fs, 100}, 10, 100},
 {{f1, 0}, 0, fs},
 {{f2, fs / (2 Pi) *  Pi/4 }, 0, fs},
 {{f3, fs / (2 Pi) *  Pi/2 }, 0, fs},
 {{a0, 0.2}, 0, 1, 0.01},
 {{a1, 0.2}, 0, 1, 0.01}
]