import ROOT
import numpy as np
import sys
import argparse

ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser()
parser.add_argument('--batch', action = 'store_true')
parser.add_argument('--label')
args = parser.parse_args()

label = args.label
batch = args.batch
ROOT.gROOT.SetBatch(batch)

can = ROOT.TCanvas()

tgun_file = ROOT.TFile.Open('tau_gentau_tuple_TGUN{}.root'.format(label), 'READ')
fake_file = ROOT.TFile.Open('tau_jet_tuple_FAKES{}.root'  .format(label), 'READ')

tree_tgun = tgun_file.Get('tree')
tree_fake = fake_file.Get('tree')

#base_selection = ' && '.join(['tau_gen_vis_pt>18', 'abs(tau_gen_vis_eta)<2.4'])
tgun_selection = ' && '.join(['tau_gen_vis_pt > 20', 'abs(tau_gen_vis_eta) < 2.3'])
fake_selection = '1'

histo_tgun = ROOT.TH1F('tgun', '', 100, 0, 1)
histo_fake = ROOT.TH1F('fake', '', 100, 0, 1)

histo_tgun.SetLineColor(ROOT.kBlue ) ; histo_tgun.SetFillColor(ROOT.kBlue ) ; histo_tgun.SetFillColorAlpha(ROOT.kBlue , 0.5)
histo_fake.SetLineColor(ROOT.kRed  ) ; histo_fake.SetFillColor(ROOT.kRed  ) ; histo_fake.SetFillColorAlpha(ROOT.kRed  , 0.5)

tree_tgun.Draw('tau_reco_byDeepTau2017v2VSjetraw >> tgun', tgun_selection)
tree_fake.Draw('tau_reco_byDeepTau2017v2VSjetraw >> fake', fake_selection)

histo_tgun.ClearUnderflowAndOverflow() ; histo_tgun.Scale(1. / histo_tgun.Integral())
histo_fake.ClearUnderflowAndOverflow() ; histo_fake.Scale(1. / histo_fake.Integral())

histo_tgun.GetYaxis().SetRangeUser(0, 1.1 * max(histo_tgun.GetMaximum(), histo_fake.GetMaximum()))
histo_fake.GetYaxis().SetRangeUser(0, 1.1 * max(histo_tgun.GetMaximum(), histo_fake.GetMaximum()))

histo_tgun.GetXaxis().SetTitle('NN score')
histo_fake.GetXaxis().SetTitle('NN score')

histo_tgun.Draw('HIST')
histo_fake.Draw('HIST SAME')

leg = ROOT.TLegend(0.4, 0.8, 0.6, 0.9)
leg.AddEntry(histo_tgun, 'TGUN' , 'f')
leg.AddEntry(histo_fake, 'FAKES', 'f')
leg.Draw('SAME')

can.SaveAs('pdf/NN_score{}.pdf'.format(label), 'pdf')