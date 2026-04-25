#
# This python macro produces a 2x2 plot following the cmsQuadPlotCanvas
# implemented as auxiliar variables.
#
# Written by O. Gonzalez (2025_08_06)
#

import math

import ROOT

import cmsstyle
import cmsstyle.cmsstyleaux as cmsstyleaux

# # # #
def test_cmsQuadHisto ():
    """Make the plot with the histograms generated on the fly.
    """

    # Producing the histograms to plot
    h1 = ROOT.TH1D("test1","test1",60,0.0,3.0)

    for i in range(1,61):
        h1.SetBinContent(i,i+2*math.cos(i))

    # Plotting the histogram

    cmsstyle.setCMSStyle()  # Setting the style

    #h1.Draw()
    #input()

    cmsstyle.SetEnergy(13.6)
    cmsstyle.SetLumi(45,"fb","Run 3",1)
    cmsstyle.SetExtraText("p")

    # Setting up the canvas with the plots

    (c,pads) = cmsstyleaux.cmsQuadPlotCanvas('QuadPlot',
                                             h1.GetXaxis().GetXmin(),
                                             h1.GetXaxis().GetXmax(),
                                             0,
                                             65,
                                             "test X",
                                             "Test Y",
                                             )

    # And plotting!

    pads[3].cd()
    cmsstyle.cmsObjectDraw(h1,"")
    pads[0].cd()
#    h1.Draw("SAME")

    cmsstyle.UpdatePad(c)
    cmsstyle.UpdatePad(pads[0])

    cmsstyle.SaveCanvas(c,"test_cmsQuadHisto.png")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For running as a shell command to get the list of files (comma-separated)
if __name__ == '__main__':
    test_cmsQuadHisto()

# #######################################################################
