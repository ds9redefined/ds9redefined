input = LSMASHVideoSource("episode.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

PD1 = inputDW.Pulldown(0, 2).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD2 = inputDW.Pulldown(0, 3).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD3 = inputDW.Pulldown(1, 3).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD4 = inputDW.Pulldown(1, 4).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD5 = inputDW.Pulldown(2, 4).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")

PD1