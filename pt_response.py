import ROOT
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("--batch", action = 'store_true')
args = parser.parse_args()
batch = args.batch
ROOT.gROOT.SetBatch(batch)
ROOT.gStyle.SetOptStat(0)


file_stdr = ROOT.TFile.Open('tau_gentau_tuple_TGUN_standard.root', 'READ')
file_0p90 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p9eff.root'  , 'READ')
file_0p05 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p95eff.root' , 'READ')
file_xchk = ROOT.TFile.Open('tau_gentau_tuple_TGUN_xcheck1e-5.root', 'READ')

histo_stdr = ROOT.TH1F('histo_stdr', '', 100, -1, 5)
histo_0p90 = ROOT.TH1F('histo_0p90', '', 100, -1, 5)
histo_0p95 = ROOT.TH1F('histo_0p95', '', 100, -1, 5)
histo_xchk = ROOT.TH1F('histo_xchk', '', 100, -1, 5)

histo_stdr.GetXaxis().SetTitle('1. - RECO_pT / GEN_vis_pT') ; histo_stdr.SetTitle('stdr')
histo_0p90.GetXaxis().SetTitle('1. - RECO_pT / GEN_vis_pT') ; histo_0p90.SetTitle('0p90')
histo_0p95.GetXaxis().SetTitle('1. - RECO_pT / GEN_vis_pT') ; histo_0p95.SetTitle('0p95')
histo_xchk.GetXaxis().SetTitle('1. - RECO_pT / GEN_vis_pT') ; histo_xchk.SetTitle('xchk')

tree_stdr = file_stdr.Get('tree')
tree_0p90 = file_0p90.Get('tree')
tree_0p95 = file_0p05.Get('tree')
tree_xchk = file_xchk.Get('tree')

base_selection = ' && '.join(['tau_gen_vis_pt > 20', 'abs(tau_gen_vis_eta) < 2.3'])
for dm in [0, 1, 2, 3, 4, 10, 11, 12, 13, 14]:
    selection = ' && '.join([base_selection, 'tau_gen_decaymode == {}'.format(dm)])
    tree_stdr.Draw('1. - (tau_reco_pt / tau_gen_vis_pt) >> histo_stdr', selection)
    tree_0p90.Draw('1. - (tau_reco_pt / tau_gen_vis_pt) >> histo_0p90', selection)
    tree_0p95.Draw('1. - (tau_reco_pt / tau_gen_vis_pt) >> histo_0p95', selection)
    tree_xchk.Draw('1. - (tau_reco_pt / tau_gen_vis_pt) >> histo_xchk', selection)

    can = ROOT.TCanvas()
    can.Divide(2, 2)

    can.cd(1) ; histo_stdr.Draw('HIST')
    can.cd(2) ; histo_0p90.Draw('HIST')
    can.cd(3) ; histo_0p95.Draw('HIST')
    can.cd(4) ; histo_xchk.Draw('HIST')

    can.SaveAs('pdf/pt_response_DM{}.pdf'.format(dm), 'pdf')
    


