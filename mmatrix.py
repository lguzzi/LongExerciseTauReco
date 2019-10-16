import ROOT
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument(
	"--batch",
    action = 'store_true')
args = parser.parse_args()
batch = args.batch
ROOT.gROOT.SetBatch(batch)
ROOT.gStyle.SetOptStat(0)


file_stdr = ROOT.TFile.Open('tau_gentau_tuple_TGUN_standard.root', 'READ')
file_0p90 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p9eff.root'  , 'READ')
file_0p05 = ROOT.TFile.Open('tau_gentau_tuple_TGUN_0p95eff.root' , 'READ')
file_xchk = ROOT.TFile.Open('tau_gentau_tuple_TGUN_xcheck1e-5.root', 'READ')

tree_stdr = file_stdr.Get('tree')
tree_0p90 = file_0p90.Get('tree')
tree_0p95 = file_0p05.Get('tree')
tree_xchk = file_xchk.Get('tree')

bins = np.array([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 700]) # variable binning

histo_stdr = ROOT.TH1F('stdr_1D', '', 12, -0.5, 11.5)
histo_0p90 = ROOT.TH1F('0p90_1D', '', 12, -0.5, 11.5)
histo_0p95 = ROOT.TH1F('0p95_1D', '', 12, -0.5, 11.5)
histo_xchk = ROOT.TH1F('xchk_1D', '', 12, -0.5, 11.5)

mmatrix_stdr = ROOT.TH2F('stdr', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_stdr.SetTitle('stdr') ; mmatrix_stdr.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_stdr.GetYaxis().SetTitle('tau_reco_decaymode')
mmatrix_0p90 = ROOT.TH2F('0p90', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_0p90.SetTitle('0p90') ; mmatrix_0p90.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_0p90.GetYaxis().SetTitle('tau_reco_decaymode')
mmatrix_0p95 = ROOT.TH2F('0p95', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_0p95.SetTitle('0p95') ; mmatrix_0p95.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_0p95.GetYaxis().SetTitle('tau_reco_decaymode')
mmatrix_xchk = ROOT.TH2F('xchk', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_xchk.SetTitle('xchk') ; mmatrix_xchk.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_xchk.GetYaxis().SetTitle('tau_reco_decaymode')

base_selection = 'tau_reco_decaymode >= 0'
for ii in range(len(bins)-1):
	selection = ' && '.join([base_selection, 'tau_gen_vis_pt >= {}'.format(bins[ii]), 'tau_gen_vis_pt < {}'.format(bins[ii+1])])
	
	tree_stdr.Draw('tau_reco_decaymode : tau_gen_decaymode >> stdr', selection, 'COL Z TEXT')
	tree_0p90.Draw('tau_reco_decaymode : tau_gen_decaymode >> 0p90', selection, 'COL Z TEXT')
	tree_0p95.Draw('tau_reco_decaymode : tau_gen_decaymode >> 0p95', selection, 'COL Z TEXT')
	tree_xchk.Draw('tau_reco_decaymode : tau_gen_decaymode >> xchk', selection, 'COL Z TEXT')

	can = ROOT.TCanvas() 
	can.Divide(2, 2)

	can.cd(1) ; mmatrix_stdr.Draw('COL Z TEXT')
	can.cd(2) ; mmatrix_0p90.Draw('COL Z TEXT')
	can.cd(3) ; mmatrix_0p95.Draw('COL Z TEXT')
	can.cd(4) ; mmatrix_xchk.Draw('COL Z TEXT')
	can.SetGridx()
	can.SetGridy()
	can.SaveAs('pdf/mmatrix_vispt_{}_{}_GeV.pdf'.format(bins[ii], bins[ii+1]), 'pdf')
