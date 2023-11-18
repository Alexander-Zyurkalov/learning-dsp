#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-11-18 *)

func[frequency_, modFrequency_, modIndex_, t_] := Module[{},
    Sin[2 Pi frequency t + modIndex * Sin[2 Pi modFrequency t]]
];


generateSound[frequency_, modFrequency_, modIndex_, duration_, sampleRate_] := Module[{},
    Table[
        func[frequency, modFrequency, modIndex, t],
        {t, 0, duration, 1/sampleRate}
    ]
];
Manipulate[
    ListPlay[generateSound[frequency, modFrequency, modIndex, duration, sampleRate], SampleRate -> sampleRate],
    {{frequency, 440}, 1, 1000},
    {{modFrequency, 440}, 1, 1000},
    {{modIndex, 1}, 0, 10}, (* Added modIndex slider *)
    {{duration, 1}, 1, 10},
    {{sampleRate, 44100}, 1000, 48000}
]
