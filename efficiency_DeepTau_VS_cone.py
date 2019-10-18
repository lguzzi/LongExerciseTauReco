import ROOT
import numpy as np
import sys
import argparse

ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser()
parser.add_argument('--type')
parser.add_argument('--batch')
parser.add_argument('--flag', default = 'tau_reco_byMediumDeepTau2017v2VSjet')

args = parser.parse_args()
sample = args.type
flag = args.flag
batch = args.batch

ROOT.gROOT.SetBatch(batch)

ntuple = 'gentau' if sample == 'TGUN' else 'jet' if sample == 'FAKES' else ''

file_stdr = ROOT.TFile.Open('tau_{}_tuple_{}_standard.root'.format(ntuple, sample), 'READ')
file_0p90 = ROOT.TFile.Open('tau_{}_tuple_{}_0p90eff.root' .format(ntuple, sample), 'READ')
file_0p05 = ROOT.TFile.Open('tau_{}_tuple_{}_0p95eff.root' .format(ntuple, sample), 'READ')

tree_stdr = file_stdr.Get('tree')
tree_0p90 = file_0p90.Get('tree')
tree_0p95 = file_0p05.Get('tree')

deep_tau_flag = flag
den_selection = ' && '.join(['tau_gen_vis_pt>18', 'abs(tau_gen_vis_eta)<2.4'])
num_selection = ' && '.join([den_selection, deep_tau_flag, 'tau_reco_decaymode >= 0', 'tau_reco_decaymode != 5', 'tau_reco_decaymode != 6'])

bins = np.array([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 700]) # variable binning
histo_den = ROOT.TH1F('den', 'den', len(bins)-1, bins)
histo_num = ROOT.TH1F('num', 'num', len(bins)-1, bins)

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

multigraph = ROOT.TMultiGraph('mgraph', '')
multigraph.Add(graph_stdr)
multigraph.Add(graph_0p90)
multigraph.Add(graph_0p95)

leg = ROOT.TLegend(0.7, 0.15, 0.95, 0.45)
leg.AddEntry(graph_stdr, 'max(min(0.1, 3. / x), 0.05) (standard, 80"%" GEN efficiency) ', 'lep')
leg.AddEntry(graph_0p90, 'max(min(0.15, 0.24 / x^{0.93}), 0.02) (90"%" GEN efficiency)', 'lep')
leg.AddEntry(graph_0p95, 'max(min(0.21, 0.45 / x^{0.91}), 0.03) (95"%" GEN efficiency)', 'lep')

c = ROOT.TCanvas("c","c")
c.SetLogx()
c.SetTitle('')

multigraph.SetTitle('DEN: {} \t NUM: {};GEN #tau vis. pT; efficiency'.format(den_selection, num_selection.replace(den_selection, '')))
multigraph.Draw('APL')
leg.Draw('SAME')

c.SetLogx()
c.SetTitle('')
c.SaveAs('pdf/{}/DeepTau_efficiency_VS_cone.pdf'.format(sample), 'pdf')