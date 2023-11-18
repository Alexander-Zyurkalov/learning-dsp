#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-11-18 *)

func[frequency_, t_] := Module[{},
    Sin[2 Pi frequency t]
];


generateSound[frequency_, duration_, sampleRate_] := Module[{},
    Table[
        func[frequency, t],
        {t, 0, duration, 1/sampleRate}
    ]
];
Manipulate[
    ListPlay[generateSound[frequency, duration, sampleRate], SampleRate -> sampleRate],
    {{frequency,440}, 1, 1000},
    {{duration, 1}, 1, 10},
    {{sampleRate, 44100}, 1000, 48000}
]

