import ROOT
import numpy as np
import root_numpy
import argparse
ROOT.gStyle.SetOptStat(0)

label = '_standard'

parser = argparse.ArgumentParser(
            description="Convert MiniAOD to flat ntuples!")
parser.add_argument(
    "--file",
    choices=['TGUN','FAKES'],
    required=True,
    help='Specify the sample you want to flatten')
args = parser.parse_args()
sample = args.file

root_file = ROOT.TFile.Open('samples/tau_gentau_tuple_{}{}.root'.format(sample, label), 'READ')
tree = root_file.Get('tree')

pt_bins = np.asarray([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 400, 700])

histo_den = ROOT.TH1F('den', 'GEN events' , len(pt_bins) - 1, pt_bins)
histo_num = ROOT.TH1F('num', 'DM>=0 events', len(pt_bins) - 1, pt_bins)

den_selection = ' && '.join(['tau_gen_vis_pt >= 18', 'abs(tau_gen_vis_eta) < 2.4'])

tree.Draw('tau_gen_vis_pt>>den', den_selection)
tree.Draw('tau_gen_vis_pt>>num', ' && '.join([den_selection, 'tau_reco_decaymode >= 0', 'tau_reco_decaymode != 5', 'tau_reco_decaymode != 6']))

c = ROOT.TCanvas()
eff = ROOT.TEfficiency(histo_num, histo_den)
eff.SetTitle('{};generator-level #tau vis. pT [GeV]; DM efficiency'.format(den_selection))
eff.SetMarkerStyle(8)
eff.Draw('APL')

leg = ROOT.TLegend(0.7, 0.2, 0.95, 0.25)
leg.AddEntry(eff, 'standard sig. cone', 'lep')
leg.Draw('SAME')

# save the current canvas
c.SetLogx()
c.SaveAs('pdf/{}_reco_efficiency{}.pdf'.format(sample, label))
c.Clear()