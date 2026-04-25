#
# This python macro produces a plot with 2-D histogram using the polar option
#
# Written by O. Gonzalez (2025_07_16)
#

import math

import ROOT

import cmsstyle
import cmsstyle.cmsstyleaux as cmsstyleaux

# # # #
def test_cmsPolarHisto ():
    """Make the plot with the histograms on the fly.

    """

    cmsstyle.setCMSStyle()  # Setting the style

    # Producing the histogram to plot
    h1 = ROOT.TH2D("test1","test1",60,0.9,3.0,60,-180.0,180.0)

    for i in range(1,61):
        phi = h1.GetXaxis().GetBinCenter(i)
        for j in range(1,61):
            h1.SetBinContent(i,j,(j/10.0)+math.cos(phi))

    # In fact we want to use other:

    f = ROOT.TFile.Open("/afs/cern.ch/work/o/oglez/user/trabajo/releases/OGNtupleProjects/2025_06/CMSSW_15_0_9/src/CMSSWCiemat/Analysis/SingleMuonTriggerStudies/ana/HighPtMuonTriggerEfficiency_2025_05/output_highptmuontrigeffic/2025_05_10_0037_post_1cad73fb4551/inputfiles/highptmuontrigeffic_JetMET_2025-MINIv6NANOv15_NANOAOD+calometTrig.root")

    h2a = f.Get("Muon53/effic_Mu50/muonPhiVSmuonEta")

    h2b = f.Get("Muon53/muonPhiVSmuonEta")

    h2a.Divide(h2b)

    h1 = ROOT.TH2D("test1","test1",21,0.9,3.0,240,-180.0,180.0)

    for j in range(1,241):
        for i in range(1,22):
            h1.SetBinContent(i,j,h2a.GetBinContent(i+39,j))

    # Plotting the histogram!
    #h1.Draw()
    #input()

    cmsstyle.SetEnergy(13.6)
    cmsstyle.SetLumi(None,"fb","2025",1)
    cmsstyle.SetExtraText("pw")

    c = cmsstyleaux.DrawPolarHistogram(h1,"#eta")

    # Some additions

    t = ROOT.TLatex(0.15,0,"Efficiency for HLT_Mu50")
    cmsstyle.cmsObjectDraw(t,'',SetNDC=1,TextSize=0.04,TextFont=42)

    cmsstyle.SaveCanvas(c,"test_cmsPolarHisto.png")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For running as a shell command to get the list of files (comma-separated)
if __name__ == '__main__':
    test_cmsPolarHisto()

# #######################################################################
