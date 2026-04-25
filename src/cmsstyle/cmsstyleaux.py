#
# This python macro produces a plot with 2-D histogram using the polar option
#
# Written by O. Gonzalez (2025_07_19)
#

import math

import ROOT

import cmsstyle

# # # #
def DrawPolarHistogram (histogram,Rvar,Rmax=None,centeredZero=True,invertedRadius=True):
    """This routine allows to draw a 2-D histogram as a polar-based histogram. The
    idea is that the Y-axis (by default) is taken as an azimuthal-kind of
    variable and plot as the azimuthal variable in the X-Y plane. The X-axis is
    taken as the radial variable (perhaps inverted).

    The plot is done in COLZ for TH2 histograms, except that the axes are
    represented as polar.
    """

    if Rmax is None:   # We just get it from the histogram, X-axis
        Rmax = histogram.GetXaxis().GetXmax()

    cmsstyle.getCMSStyle().SetTickLength(0,'X')
    cmsstyle.getCMSStyle().SetTickLength(0,'Y')

    # First we need to plot the Frame without the axis labels

    c = cmsstyle.cmsCanvas("Testing",-Rmax,Rmax,-Rmax,Rmax,
                           "",Rvar,square=True,
                           with_z_axis=True,
                           iPos=0
                           )

    cmsstyle.GetCmsCanvasHist(c).GetXaxis().SetLabelSize(0)
    cmsstyle.GetCmsCanvasHist(c).GetYaxis().SetLabelSize(0)

    c.Draw()

    cmsstyle.setCMSStyle()  # Resetting the style

    # To build the histogram to be drawn we need to be very smart
    # so the magic flows...

    c.polarHist = ROOT.TH2F("Polar","Polar",
                            histogram.GetNbinsY(),-Rmax,Rmax,
                            histogram.GetNbinsX(),-Rmax,Rmax)

    # Filling following the bins in both axis:

    nbinsy = c.polarHist.GetNbinsY()
#OLD    nbinsx = c.polarHist.GetNbinsX()
    nxlimit = int(c.polarHist.GetNbinsX()/2+1.5)  # e.g. 20 bins -> 1...10

    for ix in range(1,nbinsy+1):  # All the "radial bins"

        ibiny = nbinsy-ix+1    # ix -> ibiny

        for iy in range(1,nxlimit):
            # Need to fill TWO bins for phi... using the original code

            ibinx = nxlimit+iy-1  # Inverting bins (e.g. for positive eta.)

            c.polarHist.SetBinContent(ibinx,ibiny,histogram.GetBinContent(ix,iy))
            c.polarHist.SetBinError(ibinx,ibiny,histogram.GetBinError(ix,iy))

            c.polarHist.SetBinContent(iy,ibiny,histogram.GetBinContent(ix,ibinx))
            c.polarHist.SetBinError(iy,ibiny,histogram.GetBinError(ix,ibinx))

    # And plotting it!
#    cmsstyle.getCMSStyle().SetPalette(ROOT.kBlackBody)
#    cmsstyle.SetCMSPalette()
    cmsstyle.SetAlternative2DColor()
    ROOT.TColor.InvertPalette()

    cmsstyle.cmsObjectDraw(c.polarHist,"POLZ")

    # We add some helping axis for the radial!

    c.axis = [(ROOT.TGaxis(-Rmax,Rmax,-Rmax,0.0,
                          histogram.GetXaxis().GetXmin(),histogram.GetXaxis().GetXmax(),
                          505,"S"),-0.036),
              (ROOT.TGaxis(-Rmax,-Rmax,-Rmax,0.0,
                          histogram.GetXaxis().GetXmin(),histogram.GetXaxis().GetXmax(),
                          505,"S"),0.013),
              ]

    for xaxs in c.axis:
        xaxs[0].SetLabelOffset(xaxs[1])
        xaxs[0].SetTickLength(2*cmsstyle.getCMSStyle().GetTickLength('Y'))

        xaxs[0].SetLabelFont(histogram.GetXaxis().GetLabelFont())

        xaxs[0].Draw()

    # And some more object to help:

    c.line1 = ROOT.TLine(-Rmax,0.0,Rmax,0.0)
    c.line1.Draw()
    c.line2 = ROOT.TLine(0.0,-Rmax,0.0,Rmax)
    c.line2.Draw()

    return c

# # # #
def cmsQuadPlotCanvas (canvName,
                       x_min,x_max,y_min,y_max,
                       nameXaxis,
                       nameYaxis,
                       ):
    """Create a Canvas for 2x2 plots generating the scheme of the plot. It does
    setup the plot using the provided parameters, trying to follow the CMS
    Style as close as possible.

    Args:
        canvName (str): The name of the canvas.
        x_min (float): The minimum value of the x-axis.
        x_max (float): The maximum value of the x-axis.
        y_min (float): The minimum value of the y-axis.
        y_max (float): The maximum value of the y-axis.
        nameXaxis (str): The label for the x-axis.
        nameYaxis (str): The label for the y-axis.
    """

    # Defining the TCanvas: 600x600

    canvas = ROOT.TCanvas(canvName,"Main Canvas for the Quad (2x2) plot",600,600)

    canvas.SetTopMargin(0.07)
    canvas.SetBottomMargin(0.145)
    canvas.SetLeftMargin(0.145)
    canvas.SetRightMargin(0.05)

    # Defining The TPads for the 4 plots:

    pads=[ROOT.TPad('upperLeftPad',"Upper-Left Pad of the plot",0.0,0.52,0.55,0.93),
          ROOT.TPad('upperRightPad',"Upper-Right Pad of the plot",0.55,0.52,0.95,0.93),
          ROOT.TPad('lowerLeftPad',"Lower-Left Pad of the plot",0.0,0.0,0.55,0.52),
          ROOT.TPad('lowerRightPad',"Lower-Right Pad of the plot",0.55,0.0,0.95,0.52),
          ]

    #for xpad in pads:
    #    xpad.SetFrameFillStyle(0)

    # Specifics of the pads:
    pads[0].SetTopMargin(0.007)
    pads[0].SetBottomMargin(0.007)
    pads[0].SetRightMargin(0.007)
    pads[0].SetLeftMargin(0.29)
    pads[0].Draw('SAME')

    pads[1].SetTopMargin(0.007)
    pads[1].SetBottomMargin(0.007)
    pads[1].SetRightMargin(0.007)
    pads[1].SetLeftMargin(0.007)
    pads[1].Draw('SAME')

    pads[2].SetTopMargin(0.007)
    pads[2].SetBottomMargin(0.21)
    pads[2].SetRightMargin(0.007)
    pads[2].SetLeftMargin(0.29)
    pads[2].Draw('SAME')

    pads[3].SetTopMargin(0.007)
    pads[3].SetBottomMargin(0.21)
    pads[3].SetRightMargin(0.007)
    pads[3].SetLeftMargin(0.007)
    pads[3].Draw('SAME')

    # We modify slightly the borders to prevent overlapping of numbers

    # The pads they need a proper formatting set, scaling fonts
    # which is done with a Frame.

    ymin = y_min+0.001*(y_max-y_min)  # For all
    ymax = y_max-0.001*(y_max-y_min)
    xmin = x_min+0.001*(x_max-x_min)
    xmax = x_max-0.001*(x_max-x_min)

    frames = []
    for ip in range(0,4):
        pads[ip].cd()

        f = ROOT.gPad.DrawFrame(xmin,ymin,xmax,ymax)

        f.GetXaxis().SetTickLength(f.GetXaxis().GetTickLength()*(1.5,1.05,1.5,1.05)[ip])
        f.GetXaxis().SetLabelSize(f.GetXaxis().GetLabelSize()*(0,0,1,1.25)[ip])
        f.GetXaxis().SetLabelOffset(f.GetXaxis().GetLabelOffset()-(0,0,0,0.01)[ip])

        f.GetYaxis().SetTickLength(f.GetYaxis().GetTickLength()*(0.75,1,1,1.5)[ip])
        f.GetYaxis().SetLabelSize(f.GetYaxis().GetLabelSize()*(1.25,0,1,0)[ip])

        frames.append(f)

    # Adding the titles:

    frames[0].GetYaxis().SetTitle(nameYaxis)
    frames[0].GetYaxis().SetTitleSize(frames[0].GetYaxis().GetTitleSize()*1.5)
    frames[0].GetYaxis().SetTitleOffset(frames[0].GetYaxis().GetTitleOffset()-0.4)
    frames[3].GetXaxis().SetTitle(nameXaxis)
    frames[3].GetXaxis().SetTitleSize(frames[3].GetXaxis().GetTitleSize()*1.5)
    frames[3].GetXaxis().SetTitleOffset(frames[3].GetXaxis().GetTitleOffset()-0.3)

    # Draw CMS logo and update canvas
    cmsstyle.CMS_lumi(canvas,0,1)
    cmsstyle.UpdatePad(canvas)

    #canvas.RedrawAxis()
    for xpad in pads:
        cmsstyle.UpdatePad(xpad)
        xpad.RedrawAxis()

#    canvas.GetFrame().Draw()
    return (canvas,pads)

# # # #
def cmsTriadPlotCanvas (canvName,
                       x_min,x_max,y_min,y_max,
                       nameXaxis,
                       nameYaxis,
                       ):
    """Create a Canvas for 3x1 plots generating the scheme of the plot. It does
    setup the plot using the provided parameters, trying to follow the CMS
    Style as close as possible.

    Args:
        canvName (str): The name of the canvas.
        x_min (float): The minimum value of the x-axis.
        x_max (float): The maximum value of the x-axis.
        y_min (float): The minimum value of the y-axis.
        y_max (float): The maximum value of the y-axis.
        nameXaxis (str): The label for the x-axis.
        nameYaxis (str): The label for the y-axis.
    """

    # Defining the TCanvas: 1500x600

    canvas = ROOT.TCanvas(canvName,"Main Canvas for the Triad (3x1) plot",1500,600)

    canvas.SetTopMargin(0.07)
    canvas.SetBottomMargin(0.145)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.02)

    # Defining The TPads for the 4 plots:

    pads=[ROOT.TPad('LeftPad',"Left Pad of the plot",0.0,0.0,0.39,1.0),
          ROOT.TPad('CenterPad',"Center Pad of the plot",0.39,0.0,0.69,1.0),
          ROOT.TPad('RightPad',"Right Pad of the plot",0.69,0.0,1.0,1.0),
          ]

    #for xpad in pads:
    #    xpad.SetFrameFillStyle(0)

    # Specifics of the pads:
    pads[0].SetTopMargin(0.07)
    pads[0].SetBottomMargin(0.17)
    pads[0].SetRightMargin(0.015)
    pads[0].SetLeftMargin(0.24)
    pads[0].Draw('SAME')

    pads[1].SetTopMargin(0.07)
    pads[1].SetBottomMargin(0.17)
    pads[1].SetRightMargin(0.025)
    pads[1].SetLeftMargin(0.005)
    pads[1].Draw('SAME')

    pads[2].SetTopMargin(0.07)
    pads[2].SetBottomMargin(0.17)
    pads[2].SetRightMargin(0.055)
    pads[2].SetLeftMargin(0.0)
    pads[2].Draw('SAME')

    # We modify slightly the borders to prevent overlapping of numbers

    # The pads they need a proper formatting set, scaling fonts
    # which is done with a Frame.

    ymin = y_min+0.001*(y_max-y_min)  # For all
    ymax = y_max-0.001*(y_max-y_min)
    xmin = x_min+0.001*(x_max-x_min)
    xmax = x_max-0.001*(x_max-x_min)

    frames = []
    for ip in range(0,3):
        pads[ip].cd()

        f = ROOT.gPad.DrawFrame(xmin,ymin,xmax,ymax)

        f.GetXaxis().SetTitle(nameXaxis)

        f.GetXaxis().SetTickLength(f.GetXaxis().GetTickLength()*(1.25,1.2,1.2)[ip])
        f.GetXaxis().SetLabelSize(f.GetXaxis().GetLabelSize()*(0.9,1.1,1.1)[ip])
        f.GetXaxis().SetLabelOffset(f.GetXaxis().GetLabelOffset()-(0.01,0.02,0.02)[ip])

        f.GetXaxis().SetTitleSize(f.GetXaxis().GetTitleSize()*(0.9,1.1,1.05)[ip])
        f.GetXaxis().SetTitleOffset(f.GetXaxis().GetTitleOffset()+(0.2,-0.05,-0.05)[ip])

        # Y-axis!

        f.GetYaxis().SetTickLength(f.GetYaxis().GetTickLength()*(0.75,1,1)[ip])
        f.GetYaxis().SetLabelSize(f.GetYaxis().GetLabelSize()*(0.9,0,0)[ip])

        frames.append(f)

    # Adding the properties for the title of Y-axis:

    frames[0].GetYaxis().SetTitle(nameYaxis)
    frames[0].GetYaxis().SetTitleSize(frames[0].GetYaxis().GetTitleSize()*1.1)
    frames[0].GetYaxis().SetTitleOffset(frames[0].GetYaxis().GetTitleOffset()+0.2)

    # Draw CMS logo and update canvas
    cmsstyle.CMS_lumi(canvas,0,1)
    cmsstyle.UpdatePad(canvas)

    #canvas.RedrawAxis()
    for xpad in pads:
        cmsstyle.UpdatePad(xpad)
        xpad.RedrawAxis()

#    canvas.GetFrame().Draw()
    return (canvas,pads)

# #######################################################################
