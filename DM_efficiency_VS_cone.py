import ROOT
import numpy as np
import sys
import argparse

ROOT.TH1.SetDefaultSumw2()

def toHistogram(graph, bins, name = 'histo'):
    histo = ROOT.TH1F(name, '', len(bins)-1, bins)
    for ii, yy in enumerate(graph.GetY()):
        ey = graph.GetErrorY(ii) ## get the mean error of bin i
        histo.SetBinContent(ii+1, yy)
        histo.SetBinError(ii+1, ey)
    
    return histo

def setHistogram(histo, kColor):
    histo.GetXaxis().SetTitle('GEN #tau vis. pT')
    histo.GetYaxis().SetTitle('ratio')
    histo.SetMarkerColor(kColor)
    histo.SetMarkerStyle(7)
    histo.SetMarkerSize(2)
    histo.SetFillColor(kColor)
    histo.SetLineColor(kColor)
    histo.SetFillColorAlpha(kColor , 0.5)

ROOT.gStyle.SetOptStat(0)

file_stdr = ROOT.TFile.Open('tau_gentau_tuple_TGUN_standard.root', 'READ')
file_0p90 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p9eff.root'  , 'READ')
file_0p05 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p95eff.root' , 'READ')
file_xchk = ROOT.TFile.Open('tau_gentau_tuple_TGUN_xcheck1e-5.root', 'READ')

tree_stdr = file_stdr.Get('tree')
tree_0p90 = file_0p90.Get('tree')
tree_0p95 = file_0p05.Get('tree')
tree_xchk = file_xchk.Get('tree')

deep_tau_flag = 'tau_reco_byMediumDeepTau2017v2p1VSjet'
den_selection = ' && '.join(['tau_gen_vis_pt>18', 'abs(tau_gen_vis_eta)<2.4', 'tau_gen_decaymode > 0'])
num_selection = ' && '.join([den_selection, 'tau_reco_decaymode >= 0'])#, 'tau_reco_decaymode != 5', 'tau_reco_decaymode != 6'])

bins = np.array([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 700]) # variable binning
histo_den = ROOT.TH1F('den', 'den', len(bins)-1, bins)
histo_num = ROOT.TH1F('num', 'num', len(bins)-1, bins)

ratio_0p90eff = ROOT.TH1F('ratio_0p90eff', '', len(bins)-1, bins)
ratio_0p95eff = ROOT.TH1F('ratio_0p95eff', '', len(bins)-1, bins)

## parse the standard signal cone sample
tree_stdr.Draw('tau_gen_vis_pt >> den', den_selection)
tree_stdr.Draw('tau_gen_vis_pt >> num', num_selection)
eff_stdr = ROOT.TEfficiency(histo_num, histo_den)
graph_stdr = eff_stdr.CreateGraph()
graph_stdr.SetLineColor(ROOT.kBlack) ; graph_stdr.SetMarkerColor(ROOT.kBlack) ; graph_stdr.SetMarkerStyle(20)

## parse the 0p90 signal cone sample
tree_0p90.Draw('tau_gen_vis_pt >> den', den_selection)
tree_0p90.Draw('tau_gen_vis_pt >> num', num_selection)
eff_0p90 = ROOT.TEfficiency(histo_num, histo_den)
graph_0p90 = eff_0p90.CreateGraph()
graph_0p90.SetLineColor(ROOT.kBlue) ; graph_0p90.SetMarkerColor(ROOT.kBlue) ; graph_0p90.SetMarkerStyle(21)

## parse the 0p95 signal cone sample
tree_0p95.Draw('tau_gen_vis_pt >> den', den_selection)
tree_0p95.Draw('tau_gen_vis_pt >> num', num_selection)
eff_0p95 = ROOT.TEfficiency(histo_num, histo_den)
graph_0p95 = eff_0p95.CreateGraph()
graph_0p95.SetLineColor(ROOT.kRed) ; graph_0p95.SetMarkerColor(ROOT.kRed) ; graph_0p95.SetMarkerStyle(22)

## parse the 0p95 signal cone sample
tree_xchk.Draw('tau_gen_vis_pt >> den', den_selection)
tree_xchk.Draw('tau_gen_vis_pt >> num', num_selection)
eff_xchk = ROOT.TEfficiency(histo_num, histo_den)
graph_xchk = eff_xchk.CreateGraph()
graph_xchk.SetLineColor(ROOT.kGreen) ; graph_xchk.SetMarkerColor(ROOT.kGreen) ; graph_xchk.SetMarkerStyle(23)

histo_stdr = toHistogram(graph_stdr, bins, 'stdr_histo')
ratio_0p90 = toHistogram(graph_0p90, bins, '0p90_histo') ; ratio_0p90.Divide(ratio_0p90, histo_stdr)
ratio_0p95 = toHistogram(graph_0p95, bins, '0p95_histo') ; ratio_0p95.Divide(ratio_0p95, histo_stdr)
ratio_xchk = toHistogram(graph_xchk, bins, 'xchk_histo') ; ratio_xchk.Divide(ratio_xchk, histo_stdr)

setHistogram(ratio_0p90, ROOT.kBlue)
setHistogram(ratio_0p95, ROOT.kRed)
setHistogram(ratio_xchk, ROOT.kGreen)

multigraph = ROOT.TMultiGraph('mgraph', '')
multigraph.Add(graph_stdr)
multigraph.Add(graph_0p90)
multigraph.Add(graph_0p95)
multigraph.Add(graph_xchk)

leg = ROOT.TLegend(0.7, 0.15, 0.95, 0.45)
leg.AddEntry(graph_stdr, 'max(min(0.1, 3. / x), 0.05) (standard, 80% GEN efficiency) ', 'lep')
leg.AddEntry(graph_0p90, 'max(min(0.15, 3.59 / x^{0.93}), 0.02) (90% GEN efficiency)', 'lep')
leg.AddEntry(graph_0p95, 'max(min(0.21, 4.85 / x^{0.91}), 0.03) (95% GEN efficiency)', 'lep')
leg.AddEntry(graph_xchk, 'XCHECK cone 1.e-5', 'lep')

leg2 = ROOT.TLegend()
leg2.AddEntry(ratio_0p90, '90% eff. / standard sig. cone eff.', 'fep')
leg2.AddEntry(ratio_0p95, '95% eff. / standard sig. cone eff.', 'fep')
leg2.AddEntry(ratio_xchk, '1.e-5 sig. cone  / standard sig. cone', 'fep')

one = ROOT.TLine(bins[0], 1, bins[-1], 1) ; one.SetLineColor(ROOT.kRed)

can = ROOT.TCanvas("c","c")
can.Divide(1, 2) 
can.GetListOfPrimitives()[0].SetPad('eff_pad', '',  0., 0.30, 1., 1., 0, 0)
can.GetListOfPrimitives()[1].SetPad('rat_pad', '',  0., 0.32, 1., 0., 0, 0)

can.GetListOfPrimitives()[0].SetLogx()
can.GetListOfPrimitives()[1].SetLogx()

can.SetTitle('')

can.cd(1)

multigraph.SetTitle('DEN: {} \t NUM: {};GEN #tau vis. pT; efficiency'.format(den_selection, num_selection.replace(den_selection, '')))
multigraph.Draw('APL')
leg.Draw('SAME')

can.cd(2)
ratio_0p90.Draw('PLE3')
ratio_0p95.Draw('PLE3 SAME')
ratio_xchk.Draw('PLE3 SAME')
leg2.Draw('SAME')
one.Draw('SAME')

can.SaveAs('pdf/DM_efficiency_VS_cone.pdf')