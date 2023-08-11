#!/usr/bin/env wolframscript

fs = 100000;
maxSamples = 4 10^6;
f = 25000;
ts = 1/fs;

samplesPerCycle = fs/f;
maxNumberOfCycles = maxSamples/samplesPerCycle;

Print[maxNumberOfCycles];