#!/usr/bin/env wolframscript

(* Wolfram Script *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: alexandrzyurkalov *)
(* :Date: 2023-11-18 *)

func[frequency_, modFrequency_, modIndex_, t_] :=
    Sin[2 Pi frequency t + modIndex * Sin[2 Pi modFrequency t]];

generateSound[frequency_, modFrequency_, modIndex_, duration_, sampleRate_] :=
    Table[func[frequency, modFrequency, modIndex, t], {t, 0, duration, 1/sampleRate}];

Manipulate[
    modFrequency = frequency * 2^(modShift/12);
    sound = generateSound[frequency, modFrequency, modIndex, duration, sampleRate];
    ListPlay[sound, SampleRate -> sampleRate],
    {{frequency, 440}, 1, 1000},
    {{modShift, 0}, 0, 32, 1},
    {{modIndex, 1}, 0, 10},
    {{duration, 1}, 1, 10},
    {{sampleRate, 44100}, 1000, 48000}
]
