import ROOT
import numpy as np
import sys
import argparse

ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser(description="Plot quantities from ntuples")
parser.add_argument("--file",
		choices=['TGUN','FAKES'],
		required=True,
		help='Specify the sample you want to use for plotting')
args = parser.parse_args()
sample = args.file

label = '_standard'

infile = ROOT.TFile.Open('tau_{}_tuple_{}{}.root'.format("jet" if sample=="QCD" else "gentau", sample, label), 'read')
infile.cd()
tree = infile.Get('tree')

bins = np.array([18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150])#, 200, 700]) # variable binning
histo_den = ROOT.TH1F('den', 'den', len(bins)-1, bins)
histo_num = ROOT.TH1F('num', 'num', len(bins)-1, bins)

den_selection = ' && '.join(['tau_gen_vis_pt>20', 'abs(tau_gen_vis_eta)<2.3'])
dm_selection  = ' && '.join(['tau_reco_decaymode >= 0', 'tau_reco_decaymode != 5', 'tau_reco_decaymode != 6'])

tree.Draw('tau_gen_vis_pt >> den', den_selection)

deep_tau_flags = 	['tau_reco_by%sDeepTau2017v2p1VSjet' %ii for ii in  [	
			'VVVLoose'	, 
			'VVLoose'	, 
			'VLoose'	, 
			'Loose'		, 
			'Medium'	, 
			'Tight'		, 
			'VTight'	, 
			'VVTight'	,
]]

c = ROOT.TCanvas("c","c")
c.SetTitle('')
leg = ROOT.TLegend(0.7, 0.15, 0.95, 0.45)
multigraph = ROOT.TMultiGraph('mgraph', '')

## plot the DM efficiency
num_selection = ' && '.join([den_selection, dm_selection])
tree.Draw('tau_gen_vis_pt>>num', num_selection)
eff_DM = ROOT.TEfficiency(histo_num, histo_den)
graph_DM = eff_DM.CreateGraph()
graph_DM.SetLineColor(ROOT.kOrange) ; graph_DM.SetMarkerColor(ROOT.kOrange) ; graph_DM.SetMarkerStyle(22)

multigraph.Add(graph_DM)
leg.AddEntry(graph_DM, 'DM efficiency', 'lep')

eff_list = [ROOT.TEfficiency('eff'+dt, '', len(bins) - 1, bins) for dt in deep_tau_flags]

for ii, dt in enumerate(deep_tau_flags):
	num_selection = ' && '.join([den_selection, dt, dm_selection])
	tree.Draw('tau_gen_vis_pt >> num', num_selection)
	
	#print 'DeepTauID', dt
	#for jj in range(len(bins)-1): print '\t', '[{}, {}] GeV'.format(bins[jj], bins[jj+1]),  histo_num.GetBinContent(jj+1), histo_den.GetBinContent(jj+1)

	eff_list[ii].SetTotalHistogram(histo_den , 'f')
	eff_list[ii].SetPassedHistogram(histo_num, 'f')
	
	eff_graph = eff_list[ii].CreateGraph()

	eff_graph.SetMarkerStyle(8)
	eff_graph.SetMarkerColor(ii + 1)
	eff_graph.SetLineColor(ii + 1)

	multigraph.Add(eff_graph)

	leg.AddEntry(eff_graph, dt, 'lpe')

multigraph.SetTitle('DEN: {} \t NUM: DeepTauID + good RECO;GEN #tau vis. pT; efficiency'.format(den_selection))
multigraph.Draw('APL')
leg.Draw('SAME')

#c.SetLogx()
c.SetGridx()
c.SetGridy()
c.SetTitle('')
c.SaveAs('pdf/DeepTau_efficiency_{}{}.pdf'.format(sample, label))
c.Clear()