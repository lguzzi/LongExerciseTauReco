import ROOT
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--batch', action = 'store_true')
parser.add_argument('--merge', action = 'store_true')
parser.add_argument('--type')
args = parser.parse_args()
batch = args.batch
sample = args.type
merge = args.merge 

ntuple = 'gentau' if sample == 'TGUN' else 'jet' if sample == 'FAKES' else ''

ROOT.gROOT.SetBatch(batch)
ROOT.gStyle.SetOptStat(0)

file_stdr = ROOT.TFile.Open('tau_{}_tuple_{}_standard.root'  .format(ntuple, sample), 'READ')
file_0p90 = ROOT.TFile.Open('tau_{}_tuple_{}_0p90eff.root'   .format(ntuple, sample), 'READ')
file_0p05 = ROOT.TFile.Open('tau_{}_tuple_{}_0p95eff.root'   .format(ntuple, sample), 'READ')

tree_stdr = file_stdr.Get('tree')
tree_0p90 = file_0p90.Get('tree')
tree_0p95 = file_0p05.Get('tree')

bins = np.array([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 700]) # variable binning

histo_stdr = ROOT.TH1F('stdr_1D', '', 12, -0.5, 11.5)
histo_0p90 = ROOT.TH1F('0p90_1D', '', 12, -0.5, 11.5)
histo_0p95 = ROOT.TH1F('0p95_1D', '', 12, -0.5, 11.5)

mmatrix_stdr = ROOT.TH2F('stdr', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_stdr.SetTitle('stdr') ; mmatrix_stdr.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_stdr.GetYaxis().SetTitle('tau_reco_decaymode')
mmatrix_0p90 = ROOT.TH2F('0p90', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_0p90.SetTitle('0p90') ; mmatrix_0p90.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_0p90.GetYaxis().SetTitle('tau_reco_decaymode')
mmatrix_0p95 = ROOT.TH2F('0p95', '', 12, -0.5, 11.5, 12, -.5, 11.5) ; mmatrix_0p95.SetTitle('0p95') ; mmatrix_0p95.GetXaxis().SetTitle('tau_gen_decaymode') ; mmatrix_0p95.GetYaxis().SetTitle('tau_reco_decaymode')

files_to_merge = []

base_selection = 'tau_reco_decaymode >= 0'
for ii in range(len(bins)-1):
	selection = ' && '.join([base_selection, 'tau_gen_vis_pt >= {}'.format(bins[ii]), 'tau_gen_vis_pt < {}'.format(bins[ii+1])])
	
	tree_stdr.Draw('tau_reco_decaymode : tau_gen_decaymode >> stdr', selection, 'COL Z TEXT')
	tree_0p90.Draw('tau_reco_decaymode : tau_gen_decaymode >> 0p90', selection, 'COL Z TEXT')
	tree_0p95.Draw('tau_reco_decaymode : tau_gen_decaymode >> 0p95', selection, 'COL Z TEXT')

	mmatrix_stdr.SetTitle('{}_stdr_{}_{}_GeV'.format(sample, bins[ii], bins[ii+1]))
	mmatrix_0p90.SetTitle('{}_0p90_{}_{}_GeV'.format(sample, bins[ii], bins[ii+1]))
	mmatrix_0p95.SetTitle('{}_0p95_{}_{}_GeV'.format(sample, bins[ii], bins[ii+1]))

	can = ROOT.TCanvas() 
	can.Divide(2, 2)

	can.cd(1) ; mmatrix_stdr.Draw('COL Z TEXT')
	can.cd(2) ; mmatrix_0p90.Draw('COL Z TEXT')
	can.cd(3) ; mmatrix_0p95.Draw('COL Z TEXT')

	can.SetGridx()
	can.SetGridy()

	file_name = 'pdf/{}/mmatrix_vispt_{}_{}_GeV.pdf'.format(sample, bins[ii], bins[ii+1])
	files_to_merge.append(file_name)
	can.SaveAs(file_name, 'pdf')

if merge:
	import os
	from PyPDF2 import PdfFileMerger
	
	merger = PdfFileMerger()
	
	for pdf in files_to_merge:
		if not os.path.isfile(pdf): continue
		merger.append(pdf)
	
	merger.write('pdf/{}/mmatrix.pdf'.format(sample))
	merger.close()

	print 'INFO: merged', len(files_to_merge), 'pdf files'
	
	for pdf in files_to_merge:
		os.remove(pdf)
	
	print 'INFO: single pdf files deleted'
