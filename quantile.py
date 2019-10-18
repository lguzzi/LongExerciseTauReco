import ROOT
import pandas
import numpy as np
import root_numpy
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def loglog_pol1(x, A, B):
    return np.exp(B) * np.power(x, -A)

def inverse(y, A, B):
    return np.power(1. * np.exp(B) / y, 1./A)

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--label', default = '_delme')

args = parser.parse_args()
sample = args.file
label = args.label

root_file = ROOT.TFile.Open('samples/tau_gentau_tuple_{}{}.root'.format(sample, label), 'READ')
tree = root_file.Get('tree')

dataframe = pandas.DataFrame( root_numpy.tree2array(    tree      = tree,
                                                        branches  = ['tau_gen_vis_signal_dR', 'tau_gen_vis_pt'],
                                                        selection = 'tau_gen_decaymode > 0 && tau_gen_decaymode <= 11'))

A = 1.
B = np.log(3.)
x = [x for x in range(20, 500)]
y = [max(min(loglog_pol1(xx, A, B), 0.1), 0.05) for xx in x]
plt.plot(x, y, label = 'max(min(3. / x, 0.1), 0.05)', linewidth = 2, color = 'r', alpha = 0.5)

QTL = [0.2, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
pt_bins = [18., 20., 22., 24., 28., 32., 36., 40., 45., 50., 60., 80., 100., 150, 200, 400, 700]
pt_bins_center = [0.5*pt_bins[jj] + 0.5*pt_bins[jj+1] for jj in range(len(pt_bins) - 1 )]

for ii, qq in enumerate(QTL):
    qtl = np.array([0.] * (len(pt_bins) - 1))
    for jj in range(len(pt_bins) - 1):
        selected = dataframe[dataframe.tau_gen_vis_pt >= pt_bins[jj]	]
        selected = selected [selected .tau_gen_vis_pt <  pt_bins[jj+1]	]
        if ii == 0: 
            print '[{}, {}]'.format(pt_bins[jj], pt_bins[jj+1]) , len(selected)
        qtl[jj]  = selected['tau_gen_vis_signal_dR'].quantile(qq)
    
    if qq in [0.9, 0.95]:
        (A, B), _ = curve_fit(loglog_pol1, np.asarray(pt_bins_center), np.asarray(qtl), method = 'lm')
        dR_up = inverse(20 , A, B)
        dR_lo = inverse(100, A, B)
        y = [max(min(loglog_pol1(xx, A, B), dR_up), dR_lo) for xx in x]
        label = 'max(min({B} / x$^{{{A}}}$, {U}), {L})'.format(	B = str(np.exp(B))[:4]  ,
                                                                A = str(A)[:4]          , 
                                                                U = str(dR_up)[:4]      , 
                                                                L = str(dR_lo)[:4]      )
        plt.plot(x, y, label = label, linewidth = 2, alpha = 0.5)

    plt.plot(pt_bins_center, qtl, label = qq, linewidth = 0.3, markersize = 10)

plt.xlabel('GEN $\\tau$ vis. pT [GeV]')
plt.ylabel('GEN $\\tau$ signal cone radius')
plt.xscale('log')
plt.yscale('log')
plt.title('cone size distribution quantiles in vis. pT bins')

plt.xlim(20, 1000)
plt.grid(linestyle = '--')
plt.legend(loc = 'upper right', framealpha = 0.2)
plt.savefig('pdf/quantile.pdf',  bbox_inches="tight")
