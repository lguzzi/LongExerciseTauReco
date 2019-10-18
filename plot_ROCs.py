import ROOT
import pandas
import numpy
import root_numpy
import scikitplot
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

tgun_selection = ' && '.join(['tau_gen_vis_pt > 20', 'abs(tau_gen_vis_eta) < 2.3', 'tau_reco_byDeepTau2017v2VSjetraw >= 0'])
fake_selection = ' && '.join(['tau_reco_byDeepTau2017v2VSjetraw >= 0', 'tau_reco_pt > 20', 'tau_reco_pt < 40'])

for label in ['_standard', '_0p90eff', '_0p95eff']:
    print 'INFO: loading sample', label
    tgun_file = 'tau_gentau_tuple_TGUN{}.root'.format(label)
    fake_file = 'tau_jet_tuple_FAKES{}.root'  .format(label)

    dframe_tgun = pandas.DataFrame( root_numpy.root2array(tgun_file, branches = ['tau_reco_byDeepTau2017v2VSjetraw'], selection = tgun_selection))
    dframe_fake = pandas.DataFrame( root_numpy.root2array(fake_file, branches = ['tau_reco_byDeepTau2017v2VSjetraw'], selection = fake_selection))
    
    dframe_tgun['target'] = numpy.ones (shape = dframe_tgun['tau_reco_byDeepTau2017v2VSjetraw'].shape, dtype = numpy.int32)
    dframe_fake['target'] = numpy.zeros(shape = dframe_fake['tau_reco_byDeepTau2017v2VSjetraw'].shape, dtype = numpy.int32)

    dframe = pandas.concat([dframe_tgun, dframe_fake])

    y_true  = numpy.array(dframe['target'])
    y_score = numpy.array(dframe['tau_reco_byDeepTau2017v2VSjetraw'])

    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    if label == '_standard':
        ## get the taupog WPs
        working_points = [  'tau_reco_by%sDeepTau2017v2VSjet' %ii  for ii in  ['VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight']]
        
        dframe_tgun = pandas.DataFrame( root_numpy.root2array(tgun_file, branches = working_points, selection = tgun_selection))
        
        for ii, wp in enumerate(working_points):
            wp_tpr = 1. * len(dframe_tgun[dframe_tgun[wp] == 1]) / len(dframe_tgun)
            
            for jj, tt in enumerate(tpr): 
                if wp_tpr < tt: break
            
            wp_fpr = 0.5 * (fpr[jj] + fpr[jj-1])
            

            legend = wp.replace('tau_reco_by', '').replace('DeepTau2017v2VSjet', '')
            plt.plot(wp_fpr, wp_tpr, marker = 'o', label = legend)

    plt.plot(fpr, tpr, label = 'SAMPLE:{} - AUC: {}'.format(label, str(auc)[:5]))



plt.xlim([1.e-5, 1])
plt.ylim([1.e-5, 1])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.legend()

plt.savefig('pdf/ROCs.pdf')
    

