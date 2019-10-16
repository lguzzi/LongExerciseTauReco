import FWCore.ParameterSet.Config as cms
# trick to make python know where to look for the imports
import sys
sys.path.append('..')
from rerunTauRecoOnMiniAOD import process
import glob

label = '_standard'

runSignal = True
maxEvents = 10000

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

tau_gun_files = glob.glob('/eos/cms/store/relval/CMSSW_10_6_4_patch1/RelValTenTau_15_500/MINIAODSIM/PU25ns_106X_upgrade2018_realistic_v9_HS-v1/10000/*.root')
tau_gun_files = ['file:'+tt for tt in tau_gun_files]
if runSignal:
    readFiles.extend(tau_gun_files)
else:
    readFiles.extend([''])
process.source = cms.Source("PoolSource", fileNames=readFiles, secondaryFileNames=secFiles)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( maxEvents )
)

print('\t Max events:', process.maxEvents.input.value())
## E.G.: change the isolation cone
#process.combinatoricRecoTaus.builders[0].isolationConeSize = cms.double(0.8) # originally 0.5

## E.G.: Remove all decay modes with piZeros
#process.combinatoricRecoTaus.builders[0].decayModes = [dm for dm in process.combinatoricRecoTaus.builders[0].decayModes if dm.nPiZeros==0]

# # change the signal cone
# originally 'max(min(0.1, 3.0/pt()), 0.05)', shrinks with pt
#process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('max(min(0.15, 3.59/(pt()^0.93)), 0.02)') ## 0.90 efficiency
process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('max(min(0.21, 4.85/(pt()^0.91)), 0.03)') ## 0.95 efficiency
#process.combinatoricRecoTaus.builders[0].signalConeSize = cms.string('0.00001') ## xcheck

## Some more settings (default values given):
"""
process.combinatoricRecoTaus.builders[0].decayModes = cms.VPSet(
        cms.PSet(
            maxPiZeros = cms.uint32(0),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(1),
            nPiZeros = cms.uint32(0)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(6),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(1),
            nPiZeros = cms.uint32(1)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(5),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(1),
            nPiZeros = cms.uint32(2)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(0),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(2),
            nPiZeros = cms.uint32(0)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(3),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(2),
            nPiZeros = cms.uint32(1)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(0),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(3),
            nPiZeros = cms.uint32(0)
        ),
        cms.PSet(
            maxPiZeros = cms.uint32(3),
            maxTracks = cms.uint32(6),
            nCharged = cms.uint32(3),
            nPiZeros = cms.uint32(1)
        )
    )

process.combinatoricRecoTaus.builders[0].qualityCuts = cms.PSet(
            isolationQualityCuts = cms.PSet(
                maxDeltaZ = cms.double(0.2),
                maxTrackChi2 = cms.double(100.0),
                maxTransverseImpactParameter = cms.double(0.03),
                minGammaEt = cms.double(1.5),
                minTrackHits = cms.uint32(8),
                minTrackPixelHits = cms.uint32(0),
                minTrackPt = cms.double(1.0),
                minTrackVertexWeight = cms.double(-1.0)
            ),
            leadingTrkOrPFCandOption = cms.string('leadPFCand'),
            primaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
            pvFindingAlgo = cms.string('closestInDeltaZ'),
            recoverLeadingTrk = cms.bool(False),
            signalQualityCuts = cms.PSet(
                maxDeltaZ = cms.double(0.4),
                maxTrackChi2 = cms.double(100.0),
                maxTransverseImpactParameter = cms.double(0.1),
                minGammaEt = cms.double(1.0),
                minNeutralHadronEt = cms.double(30.0),
                minTrackHits = cms.uint32(3),
                minTrackPixelHits = cms.uint32(0),
                minTrackPt = cms.double(0.5),
                minTrackVertexWeight = cms.double(-1.0)
            ),
            vertexTrackFiltering = cms.bool(False),
            vxAssocQualityCuts = cms.PSet(
                maxTrackChi2 = cms.double(100.0),
                maxTransverseImpactParameter = cms.double(0.1),
                minGammaEt = cms.double(1.0),
                minTrackHits = cms.uint32(3),
                minTrackPixelHits = cms.uint32(0),
                minTrackPt = cms.double(0.5),
                minTrackVertexWeight = cms.double(-1.0)
            )
        )

process.hpsPFTauDiscriminationByDecayModeFindingNewDMs.decayModes(
        cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(True),
            mass = cms.bool(True),
            phi = cms.bool(True)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('1.'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(-1000.0),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(1),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(0),
        nTracksMin = cms.uint32(1)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(True),
            mass = cms.bool(True),
            phi = cms.bool(True)
        ),
        assumeStripMass = cms.double(0.1349),
        maxMass = cms.string('max(1.3, min(1.3*sqrt(pt/100.), 4.2))'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.3),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(1),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(1),
        nTracksMin = cms.uint32(1)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(True),
            mass = cms.bool(True),
            phi = cms.bool(True)
        ),
        assumeStripMass = cms.double(0.0),
        maxMass = cms.string('max(1.2, min(1.2*sqrt(pt/100.), 4.0))'),
        maxPi0Mass = cms.double(0.2),
        minMass = cms.double(0.4),
        minPi0Mass = cms.double(0.05),
        nCharged = cms.uint32(1),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(2),
        nTracksMin = cms.uint32(1)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(False),
            mass = cms.bool(False),
            phi = cms.bool(False)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('1.2'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.0),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(2),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(0),
        nTracksMin = cms.uint32(2)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(False),
            mass = cms.bool(False),
            phi = cms.bool(False)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('max(1.2, min(1.2*sqrt(pt/100.), 4.0))'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.0),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(2),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(1),
        nTracksMin = cms.uint32(2)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(False),
            mass = cms.bool(False),
            phi = cms.bool(False)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('1.5'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.8),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(3),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(0),
        nTracksMin = cms.uint32(2)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(False),
            mass = cms.bool(False),
            phi = cms.bool(False)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('1.5'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.8),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(3),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(0),
        nTracksMin = cms.uint32(2)
    ),
    cms.PSet(
        applyBendCorrection = cms.PSet(
            eta = cms.bool(False),
            mass = cms.bool(False),
            phi = cms.bool(False)
        ),
        assumeStripMass = cms.double(-1.0),
        maxMass = cms.string('1.6'),
        maxPi0Mass = cms.double(1000000000.0),
        minMass = cms.double(0.9),
        minPi0Mass = cms.double(-1000.0),
        nCharged = cms.uint32(3),
        nChargedPFCandsMin = cms.uint32(1),
        nPiZeros = cms.uint32(1),
        nTracksMin = cms.uint32(2)
    )
)

)
"""

process.output.fileName = cms.untracked.string('{}_miniAOD_rerunTauRECO{}.root'.format("TGUN" if runSignal else "FAKES", label))
