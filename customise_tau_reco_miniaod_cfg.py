import FWCore.ParameterSet.Config as cms

# trick to make python know where to look for the imports
import sys
sys.path.append('..')

# for example: here
from rerunTauRecoOnMiniAOD import process

label = '_standard'
updatedTauName = 'slimmedTausNewID'

runSignal = True # Set to False to read in QCD file instead of ZTT
sample = 'TGUN' if runSignal else 'FAKES'
maxEvents = -1

# readFiles = cms.untracked.vstring()
if runSignal: 
    readFiles = cms.untracked.vstring('file:/eos/cms/store/group/phys_tau/CMSSW_10_6_4_patch1_RelValTenTau_15_500_PU25ns_106X_upgrade2018_realistic_v9_HS_v1/25A52E71-2B61-6747-B2BA-1F51E581E6AC.root')
else:
    readFiles = cms.untracked.vstring('file:/eos/cms/store/group/phys_tau/CMSSW_10_6_4_patch1_RelValQCD_FlatPt_15_3000HS_13_UP18_PU25ns_106X_upgrade2018_realistic_v9_HS_resub_v1/1470E602-E07A-1B4A-B56F-CC2E1E42C3C6.root')
secFiles  = cms.untracked.vstring()
process.source = cms.Source( 'PoolSource', fileNames=readFiles, secondaryFileNames=secFiles)

print('\t Max events:', process.maxEvents.input.value())

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32( maxEvents ))

# print every event
process.MessageLogger.cerr.FwkReport.reportEvery = 1

##########################################################################################
# single thread for debugging
# process.options.numberOfThreads = cms.untracked.uint32(1)

##########################################################################################
# originally 'max(min(0.1, 3.0/pt()), 0.05)', shrinks with pt
process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('max(min(0.1, 3.0/pt()), 0.05)')           ## standard
#process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('max(min(0.15, 3.59/(pt()^0.93)), 0.02)') ## 0.90 efficiency
#process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('max(min(0.21, 4.85/(pt()^0.91)), 0.03)') ## 0.95 efficiency
#process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('0.00001') ## xcheck
# process.combinatoricRecoTaus.builders[0].verbosity = cms.int32(3)

##########################################################################################
process.output.outputCommands.append('keep *_'+updatedTauName+'_*_*')
process.output.fileName = cms.untracked.string('{}_miniAOD_rerunTauRECO{}.root'.format(sample, label))

# Add new TauIDs
import RecoTauTag.RecoTau.tools.runTauIdMVA as tauIdConfig
tauIdEmbedder = tauIdConfig.TauIDEmbedder(
    process, 
    cms, 
    debug = True,
    updatedTauName = updatedTauName,
    toKeep = [ 
        'newDM2017v2', 
        'deepTau2017v2', 
    ],
    inputTaus = 'selectedPatTaus',
    )
tauIdEmbedder.runTauID()

# Run DeepTau 
process.TauReco.insert(-1, process.rerunMvaIsolationSequence)
process.TauReco.insert(-1, getattr(process,updatedTauName))


# Schedule definition
# process.schedule = cms.Schedule(deeptau_process.p,process.endjob,process.outpath)
