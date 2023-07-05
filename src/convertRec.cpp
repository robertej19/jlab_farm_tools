#include "TFile.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include <string>
#include <iostream>
#include <vector>
#include "HipoChain.h"
#include "clas12reader.h"
#include <fstream>
#include <math.h>

using namespace std;

int main(int argc, char **argv){
    clas12root::HipoChain chain;

    char File[200];
    system("ls -1 *.hipo > dataFiles.txt");
    ifstream in("dataFiles.txt", ios::in);
    if(!in){
    	cerr<< "File Not Opened!" <<endl;
    	exit(1);
    }
    while( in >> File){
    	cout<<" File Name = "<<File<<endl;
    	chain.Add(File);	
    }

    TString mode = "pi0";
    if (argc==2) mode = argv[1];
    std::cout<<"The mode is "<<mode<<"."<<std::endl;

    TFile *rFile = TFile::Open("recwithgen.root","RECREATE");
    TTree *T=new TTree("T","Rec");

    Float_t beamQ;
    Float_t liveTime;
    Float_t startTime;
    Float_t RFTime;
    Int_t   helicity;
    Int_t   helicityRaw;

    // =====  proton =====
    Int_t nmb;
    Float_t Ppx[100];
    Float_t Ppy[100];
    Float_t Ppz[100];
    Float_t Pvz[100];
    Int_t Pstat[100];
    Int_t Psector[100];
    Float_t Pchi2pid[100];
    Int_t PPcalSector[100];
    Int_t PFtof1aSector[100];
    Float_t PFtof1aHitx[100];
    Float_t PFtof1aHity[100];
    Float_t PFtof1aHitz[100];
    Float_t PFtof1aTime[100];
    Float_t PFtof1aPath[100];
    Int_t PFtof1bSector[100];
    Float_t PFtof1bHitx[100];
    Float_t PFtof1bHity[100];
    Float_t PFtof1bHitz[100];
    Float_t PFtof1bTime[100];
    Float_t PFtof1bPath[100];
    Int_t PFtof2Sector[100];
    Float_t PFtof2Hitx[100];
    Float_t PFtof2Hity[100];
    Float_t PFtof2Hitz[100];
    Float_t PFtof2Time[100];
    Float_t PFtof2Path[100];
    Float_t PCtofHitx[100];
    Float_t PCtofHity[100];
    Float_t PCtofHitz[100];
    Float_t PCtofTime[100];
    Float_t PCtofPath[100];
    Float_t PDc1Hitx[100];
    Float_t PDc1Hity[100];
    Float_t PDc1Hitz[100];
    Float_t PDc2Hitx[100];
    Float_t PDc2Hity[100];
    Float_t PDc2Hitz[100];
    Float_t PDc3Hitx[100];
    Float_t PDc3Hity[100];
    Float_t PDc3Hitz[100];
    Float_t PCvt1Hitx[100];
    Float_t PCvt1Hity[100];
    Float_t PCvt1Hitz[100];
    Float_t PCvt3Hitx[100];
    Float_t PCvt3Hity[100];
    Float_t PCvt3Hitz[100];
    Float_t PCvt5Hitx[100];
    Float_t PCvt5Hity[100];
    Float_t PCvt5Hitz[100];
    Float_t PCvt7Hitx[100];
    Float_t PCvt7Hity[100];
    Float_t PCvt7Hitz[100];
    Float_t PCvt12Hitx[100];
    Float_t PCvt12Hity[100];
    Float_t PCvt12Hitz[100];
    Int_t PNDFtrack[100];
    Float_t Pchi2track[100];

    Float_t GenPpx;
    Float_t GenPpy;
    Float_t GenPpz;
    // ==== electron =====
    Float_t Epx;
    Float_t Epy;
    Float_t Epz;
    Float_t Evx;
    Float_t Evy;
    Float_t Evz;
    Int_t Estat;
    Int_t Esector;
    Float_t EDc1Hitx;
    Float_t EDc1Hity;
    Float_t EDc1Hitz;
    // Float_t EDc2Hitx;
    // Float_t EDc2Hity;
    // Float_t EDc2Hitz;
    Float_t EDc3Hitx;
    Float_t EDc3Hity;
    Float_t EDc3Hitz;
    Float_t Eedep;
    Float_t Eedep1;
    Float_t Eedep2;
    Float_t Eedep3;

    Float_t GenEpx;
    Float_t GenEpy;
    Float_t GenEpz;
    Float_t GenEvx;
    Float_t GenEvy;
    Float_t GenEvz;

    // ==== gammas =====
    Int_t nmg;
    Float_t Gpx[100];
    Float_t Gpy[100];
    Float_t Gpz[100];
    Int_t Gstat[100];
    Int_t Gsector[100];
    Float_t Gedep[100];
    Float_t Gedep1[100];
    Float_t Gedep2[100];
    Float_t Gedep3[100];
    Float_t GcX[100];
    Float_t GcY[100];
    Float_t Gpath[100];
    Float_t Gtime[100];

    Int_t nmG;
    Float_t GenGpx[2];
    Float_t GenGpy[2];
    Float_t GenGpz[2];

    // ==== pi0s =====
    Float_t GenPipx;
    Float_t GenPipy;
    Float_t GenPipz; 

    Int_t Before[100];
    Int_t PcalSector[100];
    Int_t Ftof1aSector[100];
    Int_t Ftof1bSector[100];
    Int_t Ftof2Sector[100];

    ///   protons ================================== 
    T->Branch("nmb",&nmb,"nmb/I");
    T->Branch("Ppx",&Ppx,"Ppx[nmb]/F");
    T->Branch("Ppy",&Ppy,"Ppy[nmb]/F");
    T->Branch("Ppz",&Ppz,"Ppz[nmb]/F");
    T->Branch("Pvz",&Pvz,"Pvz[nmb]/F");
    T->Branch("Pstat",&Pstat,"Pstat[nmb]/I");
    T->Branch("Psector",&Psector,"Psector[nmb]/I");
    T->Branch("Pchi2pid",&Pchi2pid,"Pchi2pid[nmb]/F");
    T->Branch("PPcalSector",&PPcalSector,"PPcalSector[nmb]/I");
    T->Branch("PFtof1aSector",&PFtof1aSector,"PFtof1aSector[nmb]/I");
    T->Branch("PFtof1aHitx",&PFtof1aHitx,"PFtof1aHitx[nmb]/F");
    T->Branch("PFtof1aHity",&PFtof1aHity,"PFtof1aHity[nmb]/F");
    T->Branch("PFtof1aHitz",&PFtof1aHitz,"PFtof1aHitz[nmb]/F");
    T->Branch("PFtof1aTime",&PFtof1aTime,"PFtof1aTime[nmb]/F");
    T->Branch("PFtof1aPath",&PFtof1aPath,"PFtof1aPath[nmb]/F");
    T->Branch("PFtof1bSector",&PFtof1bSector,"PFtof1bSector[nmb]/I");
    T->Branch("PFtof1bHitx",&PFtof1bHitx,"PFtof1bHitx[nmb]/F");
    T->Branch("PFtof1bHity",&PFtof1bHity,"PFtof1bHity[nmb]/F");
    T->Branch("PFtof1bHitz",&PFtof1bHitz,"PFtof1bHitz[nmb]/F");
    T->Branch("PFtof1bTime",&PFtof1bTime,"PFtof1bTime[nmb]/F");
    T->Branch("PFtof1bPath",&PFtof1bPath,"PFtof1bPath[nmb]/F");
    T->Branch("PFtof2Sector",&PFtof2Sector,"PFtof2Sector[nmb]/I");
    T->Branch("PFtof2Hitx",&PFtof2Hitx,"PFtof2Hitx[nmb]/F");
    T->Branch("PFtof2Hity",&PFtof2Hity,"PFtof2Hity[nmb]/F");
    T->Branch("PFtof2Hitz",&PFtof2Hitz,"PFtof2Hitz[nmb]/F");
    T->Branch("PFtof2Time",&PFtof2Time,"PFtof2Time[nmb]/F");
    T->Branch("PFtof2Path",&PFtof2Path,"PFtof2Path[nmb]/F");
    T->Branch("PCtofHitx",&PCtofHitx,"PCtofHitx[nmb]/F");
    T->Branch("PCtofHity",&PCtofHity,"PCtofHity[nmb]/F");
    T->Branch("PCtofHitz",&PCtofHitz,"PCtofHitz[nmb]/F");
    T->Branch("PCtofTime",&PCtofTime,"PCtofTime[nmb]/F");
    T->Branch("PCtofPath",&PCtofPath,"PCtofPath[nmb]/F");
    T->Branch("PDc1Hitx",&PDc1Hitx,"PDc1Hitx[nmb]/F");
    T->Branch("PDc1Hity",&PDc1Hity,"PDc1Hity[nmb]/F");
    T->Branch("PDc1Hitz",&PDc1Hitz,"PDc1Hitz[nmb]/F");
    T->Branch("PDc2Hitx",&PDc2Hitx,"PDc2Hitx[nmb]/F");
    T->Branch("PDc2Hity",&PDc2Hity,"PDc2Hity[nmb]/F");
    T->Branch("PDc2Hitz",&PDc2Hitz,"PDc2Hitz[nmb]/F");
    T->Branch("PDc3Hitx",&PDc3Hitx,"PDc3Hitx[nmb]/F");
    T->Branch("PDc3Hity",&PDc3Hity,"PDc3Hity[nmb]/F");
    T->Branch("PDc3Hitz",&PDc3Hitz,"PDc3Hitz[nmb]/F");
    T->Branch("PCvt1Hitx",&PCvt1Hitx,"PCvt1Hitx[nmb]/F");
    T->Branch("PCvt1Hity",&PCvt1Hity,"PCvt1Hity[nmb]/F");
    T->Branch("PCvt1Hitz",&PCvt1Hitz,"PCvt1Hitz[nmb]/F");
    T->Branch("PCvt3Hitx",&PCvt3Hitx,"PCvt3Hitx[nmb]/F");
    T->Branch("PCvt3Hity",&PCvt3Hity,"PCvt3Hity[nmb]/F");
    T->Branch("PCvt3Hitz",&PCvt3Hitz,"PCvt3Hitz[nmb]/F");
    T->Branch("PCvt5Hitx",&PCvt5Hitx,"PCvt5Hitx[nmb]/F");
    T->Branch("PCvt5Hity",&PCvt5Hity,"PCvt5Hity[nmb]/F");
    T->Branch("PCvt5Hitz",&PCvt5Hitz,"PCvt5Hitz[nmb]/F");
    T->Branch("PCvt7Hitx",&PCvt7Hitx,"PCvt7Hitx[nmb]/F");
    T->Branch("PCvt7Hity",&PCvt7Hity,"PCvt7Hity[nmb]/F");
    T->Branch("PCvt7Hitz",&PCvt7Hitz,"PCvt7Hitz[nmb]/F");
    T->Branch("PCvt12Hitx",&PCvt12Hitx,"PCvt12Hitx[nmb]/F");
    T->Branch("PCvt12Hity",&PCvt12Hity,"PCvt12Hity[nmb]/F");
    T->Branch("PCvt12Hitz",&PCvt12Hitz,"PCvt12Hitz[nmb]/F");
    T->Branch("Pchi2track",&Pchi2track,"Pchi2track[nmb]/F");
    T->Branch("PNDFtrack",&PNDFtrack,"PNDFtrack[nmb]/I");

    // ===============    Electrons ==============    
    T->Branch("Epx",&Epx,"Epx/F");
    T->Branch("Epy",&Epy,"Epy/F");
    T->Branch("Epz",&Epz,"Epz/F");
    T->Branch("Evx",&Evx,"Evx/F");
    T->Branch("Evy",&Evy,"Evy/F");
    T->Branch("Evz",&Evz,"Evz/F");
    T->Branch("Estat",&Estat,"Estat/I");
    T->Branch("Esector",&Esector,"Esector/I");
    T->Branch("EDc1Hitx",&EDc1Hitx,"EDc1Hitx/F");
    T->Branch("EDc1Hity",&EDc1Hity,"EDc1Hity/F");
    T->Branch("EDc1Hitz",&EDc1Hitz,"EDc1Hitz/F");
    // T->Branch("EDc2Hitx",&EDc2Hitx,"EDc2Hitx/F");
    // T->Branch("EDc2Hity",&EDc2Hity,"EDc2Hity/F");
    // T->Branch("EDc2Hitz",&EDc2Hitz,"EDc2Hitz/F");
    T->Branch("EDc3Hitx",&EDc3Hitx,"EDc3Hitx/F");
    T->Branch("EDc3Hity",&EDc3Hity,"EDc3Hity/F");
    T->Branch("EDc3Hitz",&EDc3Hitz,"EDc3Hitz/F");
    T->Branch("Eedep",&Eedep,"Eedep/F");
    T->Branch("Eedep1",&Eedep1,"Eedep1/F");
    T->Branch("Eedep2",&Eedep2,"Eedep2/F");
    T->Branch("Eedep3",&Eedep3,"Eedep3/F");

    // ================   Gamma  ===============    
    T->Branch("nmg",&nmg,"nmg/I");
    T->Branch("Gpx",&Gpx,"Gpx[nmg]/F");
    T->Branch("Gpy",&Gpy,"Gpy[nmg]/F");
    T->Branch("Gpz",&Gpz,"Gpz[nmg]/F");
    T->Branch("Gstat",&Gstat,"Gstat[nmg]/I");
    T->Branch("Gsector",&Gsector,"Gsector[nmg]/I");
    T->Branch("Gedep",&Gedep,"Gedep[nmg]/F");
    T->Branch("Gedep1",&Gedep1,"Gedep1[nmg]/F");
    T->Branch("Gedep2",&Gedep2,"Gedep2[nmg]/F");
    T->Branch("Gedep3",&Gedep3,"Gedep3[nmg]/F");
    T->Branch("GcX",&GcX,"GcX[nmg]/F");
    T->Branch("GcY",&GcY,"GcY[nmg]/F");
    T->Branch("Gpath",&Gpath,"Gpath[nmg]/F");
    T->Branch("Gtime",&Gtime,"Gtime[nmg]/F");

    //=================  Logs =============
    T->Branch("beamQ",&beamQ,"beamQ/F");
    T->Branch("liveTime",&liveTime,"liveTime/F");
    T->Branch("startTime",&startTime,"startTime/F");
    T->Branch("RFTime",&RFTime,"RFTime/F");
    T->Branch("helicity",&helicity,"helicity/I");
    T->Branch("helicityRaw",&helicityRaw,"helicityRaw/I");


    // MC bank
    T->Branch("GenEpx",&GenEpx,"GenEpx/F");
    T->Branch("GenEpy",&GenEpy,"GenEpy/F");
    T->Branch("GenEpz",&GenEpz,"GenEpz/F");
    T->Branch("GenEvx",&GenEvx,"GenEvx/F");
    T->Branch("GenEvy",&GenEvy,"GenEvy/F");
    T->Branch("GenEvz",&GenEvz,"GenEvz/F");
    T->Branch("GenPpx",&GenPpx,"GenPpx/F");
    T->Branch("GenPpy",&GenPpy,"GenPpy/F");
    T->Branch("GenPpz",&GenPpz,"GenPpz/F");
    T->Branch("nmG", &nmG, "nmG/I");
    T->Branch("GenGpx",&GenGpx,"GenGpx[nmG]/F");
    T->Branch("GenGpy",&GenGpy,"GenGpy[nmG]/F");
    T->Branch("GenGpz",&GenGpz,"GenGpz[nmG]/F");
    T->Branch("GenPipx",&GenPipx,"GenPipx/F");
    T->Branch("GenPipy",&GenPipy,"GenPipy/F");
    T->Branch("GenPipz",&GenPipz,"GenPipz/F"); 


    //loop over files
    for(int ifile=0; ifile<chain.GetNFiles();++ifile){
        clas12::clas12reader c12{chain.GetFileName(ifile).Data()};

        //  Event bank
        auto idx_RECEv = c12.addBank("REC::Event");
        auto aBeamQ = c12.getBankOrder(idx_RECEv,"beamCharge");
        auto aLiveT = c12.getBankOrder(idx_RECEv,"liveTime");
        auto aStarT = c12.getBankOrder(idx_RECEv,"startTime");
        auto aRFTim = c12.getBankOrder(idx_RECEv,"RFTime");
        auto aHelic = c12.getBankOrder(idx_RECEv,"helicity");
        auto aHeRaw = c12.getBankOrder(idx_RECEv,"helicityRaw");

        // main particle bank ========
        auto idx_RECPart = c12.addBank("REC::Particle");
        auto iPid = c12.getBankOrder(idx_RECPart,"pid");
        auto iPx  = c12.getBankOrder(idx_RECPart,"px");
        auto iPy  = c12.getBankOrder(idx_RECPart,"py");
        auto iPz  = c12.getBankOrder(idx_RECPart,"pz");
        auto iVx  = c12.getBankOrder(idx_RECPart,"vx");
        auto iVy  = c12.getBankOrder(idx_RECPart,"vy");
        auto iVz  = c12.getBankOrder(idx_RECPart,"vz");
        auto iStat = c12.getBankOrder(idx_RECPart,"status");
        auto iChi2pid = c12.getBankOrder(idx_RECPart,"chi2pid");
        //===================


        //  Filter bank created by Sangbaek
        auto idx_FILTER = c12.addBank("FILTER::Index");
        auto iInd = c12.getBankOrder(idx_FILTER,"before");
        auto iPcalSector = c12.getBankOrder(idx_FILTER, "pcal_sector");
        auto iFtof1aSector = c12.getBankOrder(idx_FILTER, "ftof1a_sector");
        auto iFtof1bSector = c12.getBankOrder(idx_FILTER, "ftof1b_sector");
        auto iFtof2Sector = c12.getBankOrder(idx_FILTER, "ftof2_sector");
        //=========

        // Read banks: with DC, CVT, FTOF, LTCC, HTCC, ECAL, CTOF, CND 
        auto idx_Traj = c12.addBank("REC::Traj");
        auto iPindex = c12.getBankOrder(idx_Traj,"pindex");
        auto iDetector = c12.getBankOrder(idx_Traj,"detector");
        auto iLayer = c12.getBankOrder(idx_Traj,"layer");
        auto iX = c12.getBankOrder(idx_Traj,"x");
        auto iY = c12.getBankOrder(idx_Traj,"y");
        auto iZ = c12.getBankOrder(idx_Traj,"z");
        // ========================

        // Scintillator bank
        auto idx_RECScint = c12.addBank("REC::Scintillator");
        auto jPindex = c12.getBankOrder(idx_RECScint,"pindex");
        auto jDet = c12.getBankOrder(idx_RECScint,"detector");
        auto jSec = c12.getBankOrder(idx_RECScint,"sector");
        auto jLay = c12.getBankOrder(idx_RECScint,"layer");
        auto jTim = c12.getBankOrder(idx_RECScint,"time");
        auto jPat = c12.getBankOrder(idx_RECScint,"path");
        auto jX   = c12.getBankOrder(idx_RECScint,"x");
        auto jY = c12.getBankOrder(idx_RECScint,"y");
        auto jZ = c12.getBankOrder(idx_RECScint,"z");

        // REC::Track 
        auto ldx_Track = c12.addBank("REC::Track");
        auto lPindex = c12.getBankOrder(ldx_Track,"pindex");
        auto lDetector = c12.getBankOrder(ldx_Track,"detector");
        auto lsector = c12.getBankOrder(ldx_Track,"sector");
        auto lq = c12.getBankOrder(ldx_Track,"q");
        auto lchi2 = c12.getBankOrder(ldx_Track,"chi2");
        auto lNDF = c12.getBankOrder(ldx_Track,"NDF");
        // ========================

        // Read banks: Calorimeter
        auto mdx_Calo = c12.addBank("REC::Calorimeter");
        auto mPindex = c12.getBankOrder(mdx_Calo,"pindex");
        auto mDetector = c12.getBankOrder(mdx_Calo,"detector");
        auto msector = c12.getBankOrder(mdx_Calo,"sector");
        auto mLayer = c12.getBankOrder(mdx_Calo,"layer");
        auto menergy = c12.getBankOrder(mdx_Calo,"energy");
        auto mtime = c12.getBankOrder(mdx_Calo,"time");
        auto mpath = c12.getBankOrder(mdx_Calo,"path");
        auto mchi2 = c12.getBankOrder(mdx_Calo,"chi2");
        auto mx = c12.getBankOrder(mdx_Calo,"x");
        auto my = c12.getBankOrder(mdx_Calo,"y");
        auto mz = c12.getBankOrder(mdx_Calo,"z");

        // Read banks: FT
        auto ndx_FT = c12.addBank("REC::ForwardTagger");
        auto nPindex = c12.getBankOrder(ndx_FT,"pindex");
        auto nDetector = c12.getBankOrder(ndx_FT,"detector");
        auto nLayer = c12.getBankOrder(ndx_FT,"layer");
        auto nenergy = c12.getBankOrder(ndx_FT,"energy");
        auto ntime = c12.getBankOrder(ndx_FT,"time");
        auto npath = c12.getBankOrder(ndx_FT,"path");
        auto nchi2 = c12.getBankOrder(ndx_FT,"chi2");
        auto nradius = c12.getBankOrder(ndx_FT,"radius");
        auto nx = c12.getBankOrder(ndx_FT,"x");
        auto ny = c12.getBankOrder(ndx_FT,"y");
        auto nz = c12.getBankOrder(ndx_FT,"z");

        // MC bank
        auto idx_GenPart = c12.addBank("MC::Particle");
        auto iGenPid = c12.getBankOrder(idx_GenPart,"pid");
        auto iGenPx  = c12.getBankOrder(idx_GenPart,"px");
        auto iGenPy  = c12.getBankOrder(idx_GenPart,"py");
        auto iGenPz  = c12.getBankOrder(idx_GenPart,"pz");
        auto iGenVx  = c12.getBankOrder(idx_GenPart,"vx");
        auto iGenVy  = c12.getBankOrder(idx_GenPart,"vy");
        auto iGenVz  = c12.getBankOrder(idx_GenPart,"vz");

        while(c12.next() == true){

            nmb=0;
            nmg=0;
            nmG=0;

            //FILTER::Index
            for(auto ipa = 0;ipa<c12.getBank(idx_FILTER)->getRows();ipa++){
                auto val = c12.getBank(idx_FILTER)->getInt(iInd,ipa);
                auto tempPcalSector = c12.getBank(idx_FILTER)->getInt(iPcalSector,ipa);
                auto tempFtof1aSector = c12.getBank(idx_FILTER)->getInt(iFtof1aSector,ipa);
                auto tempFtof1bSector = c12.getBank(idx_FILTER)->getInt(iFtof1bSector,ipa);
                auto tempFtof2Sector = c12.getBank(idx_FILTER)->getInt(iFtof2Sector,ipa);
                Before[ipa] = val;
                PcalSector[ipa] = tempPcalSector;
                Ftof1aSector[ipa] = tempFtof1aSector;
                Ftof1bSector[ipa] = tempFtof1bSector;
                Ftof2Sector[ipa] = tempFtof2Sector;
            }

            //MC::Particle
            for(auto ipa=0;ipa<c12.getBank(idx_GenPart)->getRows();ipa++){
                auto tGenPx = c12.getBank(idx_GenPart)->getFloat(iGenPx,ipa);
                auto tGenPy = c12.getBank(idx_GenPart)->getFloat(iGenPy,ipa);
                auto tGenPz = c12.getBank(idx_GenPart)->getFloat(iGenPz,ipa);
                auto tGenVx = c12.getBank(idx_GenPart)->getFloat(iGenVx,ipa);
                auto tGenVy = c12.getBank(idx_GenPart)->getFloat(iGenVy,ipa);
                auto tGenVz = c12.getBank(idx_GenPart)->getFloat(iGenVz,ipa);

                if( (c12.getBank(idx_GenPart)->getInt(iGenPid,ipa)) == 11  ){  // electrons
                    GenEpx = tGenPx;
                    GenEpy = tGenPy;
                    GenEpz = tGenPz;
                    GenEvx = tGenVx;
                    GenEvy = tGenVy;
                    GenEvz = tGenVz;
                }

                if((c12.getBank(idx_GenPart)->getInt(iGenPid,ipa)) == 2212  ){  // protons
                    GenPpx = tGenPx;
                    GenPpy = tGenPy;
                    GenPpz = tGenPz;
                }
                        
                if((c12.getBank(idx_GenPart)->getInt(iGenPid,ipa)) == 22  ){  // photons
                    GenGpx[nmG] = tGenPx;
                    GenGpy[nmG] = tGenPy;
                    GenGpz[nmG] = tGenPz;
                nmG++;
                }

                if((c12.getBank(idx_GenPart)->getInt(iGenPid,ipa)) == 111  ){  // pi0s
                    GenPipx = tGenPx;
                    GenPipy = tGenPy;
                    GenPipz = tGenPz;
                }
            }

            // REC::Particle
            for(auto ipa=0;ipa<c12.getBank(idx_RECPart)->getRows();ipa++){

                auto tPx = c12.getBank(idx_RECPart)->getFloat(iPx,ipa);
                auto tPy = c12.getBank(idx_RECPart)->getFloat(iPy,ipa);
                auto tPz = c12.getBank(idx_RECPart)->getFloat(iPz,ipa);
                auto tVx = c12.getBank(idx_RECPart)->getFloat(iVx,ipa);
                auto tVy = c12.getBank(idx_RECPart)->getFloat(iVy,ipa);
                auto tVz = c12.getBank(idx_RECPart)->getFloat(iVz,ipa);
                auto tStat = c12.getBank(idx_RECPart)->getInt(iStat,ipa);
                auto tChi2pid = c12.getBank(idx_RECPart)->getFloat(iChi2pid,ipa);

                if( (c12.getBank(idx_RECPart)->getInt(iPid,ipa)) == 11  ){  // electrons
                    Epx = tPx;
                    Epy = tPy;
                    Epz = tPz;
                    Evx = tVx;
                    Evy = tVy;
                    Evz = tVz;
                    Esector = PcalSector[ipa];
                    EDc1Hitx = -100000;
                    EDc1Hity = -100000;
                    EDc1Hitz = -100000;
                    // EDc2Hitx = -100000;
                    // EDc2Hity = -100000;
                    // EDc2Hitz = -100000;
                    EDc3Hitx = -100000;
                    EDc3Hity = -100000;
                    EDc3Hitz = -100000;
                    Eedep = 0;
                    Eedep1 = 0;
                    Eedep2 = 0;
                    Eedep3 = 0;

                    // DC Bank (REC::Traj)        //
                    for(auto ipa2 = 0; ipa2<c12.getBank(idx_Traj)->getRows();ipa2++){

                        auto tempPnd_dc = c12.getBank(idx_Traj)->getInt(iPindex,ipa2);
                        auto tempDet_dc = c12.getBank(idx_Traj)->getInt(iDetector,ipa2);    
                        auto tempLay_dc = c12.getBank(idx_Traj)->getInt(iLayer,ipa2); 
                        auto tempX_dc = c12.getBank(idx_Traj)->getFloat(iX,ipa2); 
                        auto tempY_dc = c12.getBank(idx_Traj)->getFloat(iY,ipa2); 
                        auto tempZ_dc = c12.getBank(idx_Traj)->getFloat(iZ,ipa2);

                        if (tempPnd_dc == Before[ipa]){
                            if (tempDet_dc == 6 ){// dc{
                                if (tempLay_dc == 6){ //r1
                                    EDc1Hitx = tempX_dc;
                                    EDc1Hity = tempY_dc;
                                    EDc1Hitz = tempZ_dc;
                                }

                                // if (tempLay_dc == 18){ //r2
                                //     EDc2Hitx = tempX_dc;
                                //     EDc2Hity = tempY_dc;
                                //     EDc2Hitz = tempZ_dc;
                                // }

                                if (tempLay_dc == 36){ //r3
                                    EDc3Hitx = tempX_dc;
                                    EDc3Hity = tempY_dc;
                                    EDc3Hitz = tempZ_dc;
                                }
                            }
                        }
                    }// end of DC

                    // EC Bank (REC::Calorimeter)        //
                    for(auto ipa3 = 0; ipa3<c12.getBank(mdx_Calo)->getRows();ipa3++){
                        auto tempPnd_Calo = c12.getBank(mdx_Calo)->getInt(mPindex,ipa3);
                        auto tempDet_Calo = c12.getBank(mdx_Calo)->getInt(mDetector,ipa3);    
                        auto tempLay_Calo = c12.getBank(mdx_Calo)->getInt(mLayer,ipa3); 
                        auto tempE_Calo = c12.getBank(mdx_Calo)->getFloat(menergy,ipa3); 
                        auto tempTime_Calo = c12.getBank(mdx_Calo)->getFloat(mtime,ipa3); 
                        if (tempPnd_Calo == Before[ipa]){
                            if (tempLay_Calo == 1) Eedep1 = tempE_Calo;
                            if (tempLay_Calo == 4) Eedep2 = tempE_Calo;
                            if (tempLay_Calo == 7) Eedep3 = tempE_Calo;
                            Eedep += tempE_Calo;
                        }
                    }//end of EC
                }// end of electrons
                    
                if((c12.getBank(idx_RECPart)->getInt(iPid,ipa)) == 2212 ){  // protons

                    Ppx[nmb] = tPx;
                    Ppy[nmb] = tPy;
                    Ppz[nmb] = tPz;
                    Pvz[nmb] = tVz;
                    Pstat[nmb] = tStat;
                    Pchi2pid[nmb] = tChi2pid;
                    if (Pstat[nmb] >4000) Psector[nmb] = Pstat[nmb];
                    else if (Ftof1aSector[ipa]>0) Psector[nmb] = Ftof1aSector[ipa];	
                    else if (Ftof1bSector[ipa]>0) Psector[nmb] = Ftof1bSector[ipa];	
                    else if (Ftof2Sector[ipa]>0) Psector[nmb] = Ftof2Sector[ipa];	
                    PPcalSector[nmb] = PcalSector[ipa];
                    PFtof1aSector[nmb] = Ftof1aSector[ipa];
                    PFtof1bSector[nmb] = Ftof1bSector[ipa];
                    PFtof2Sector[nmb] = Ftof2Sector[ipa];

                    PFtof1aHitx[nmb] = -100000;
                    PFtof1aHity[nmb] = -100000;
                    PFtof1aHitz[nmb] = -100000;
                    PFtof1aTime[nmb] = -100000;
                    PFtof1aPath[nmb] = -100000;
                    PFtof1bHitx[nmb] = -100000;
                    PFtof1bHity[nmb] = -100000;
                    PFtof1bHitz[nmb] = -100000;
                    PFtof1bTime[nmb] = -100000;
                    PFtof1bPath[nmb] = -100000;
                    PFtof2Hitx[nmb] = -100000;
                    PFtof2Hity[nmb] = -100000;
                    PFtof2Hitz[nmb] = -100000;
                    PFtof2Time[nmb] = -100000;
                    PFtof2Path[nmb] = -100000;
                    PCtofHitx[nmb] = -100000;
                    PCtofHity[nmb] = -100000;
                    PCtofHitz[nmb] = -100000;
                    PCtofTime[nmb] = -100000;
                    PCtofPath[nmb] = -100000;
                    PDc1Hitx[nmb] = -100000;
                    PDc1Hity[nmb] = -100000;
                    PDc1Hitz[nmb] = -100000;
                    PDc2Hitx[nmb] = -100000;
                    PDc2Hity[nmb] = -100000;
                    PDc2Hitz[nmb] = -100000;
                    PDc3Hitx[nmb] = -100000;
                    PDc3Hity[nmb] = -100000;
                    PDc3Hitz[nmb] = -100000;
                    PCvt1Hitx[nmb] = -100000;
                    PCvt1Hity[nmb] = -100000;
                    PCvt1Hitz[nmb] = -100000;
                    PCvt3Hitx[nmb] = -100000;
                    PCvt3Hity[nmb] = -100000;
                    PCvt3Hitz[nmb] = -100000;
                    PCvt5Hitx[nmb] = -100000;
                    PCvt5Hity[nmb] = -100000;
                    PCvt5Hitz[nmb] = -100000;
                    PCvt7Hitx[nmb] = -100000;
                    PCvt7Hity[nmb] = -100000;
                    PCvt7Hitz[nmb] = -100000;
                    PCvt12Hitx[nmb] = -100000;
                    PCvt12Hity[nmb] = -100000;
                    PCvt12Hitz[nmb] = -100000;

                    // Scintillaror Bank        //
                    for(auto ipa1 = 0; ipa1<c12.getBank(idx_RECScint)->getRows();ipa1++){

                        auto tempPnd = c12.getBank(idx_RECScint)->getInt(jPindex,ipa1);
                        auto tempDet = c12.getBank(idx_RECScint)->getInt(jDet,ipa1);    
                        auto tempLay = c12.getBank(idx_RECScint)->getInt(jLay,ipa1); 
                        auto tempTim = c12.getBank(idx_RECScint)->getFloat(jTim,ipa1); 
                        auto tempPat = c12.getBank(idx_RECScint)->getFloat(jPat,ipa1); 
                        auto tempX= c12.getBank(idx_RECScint)->getFloat(jX,ipa1); 
                        auto tempY = c12.getBank(idx_RECScint)->getFloat(jY,ipa1); 
                        auto tempZ = c12.getBank(idx_RECScint)->getFloat(jZ,ipa1);


                        if (tempPnd == Before[ipa]){

                            if (tempDet == 12 ){// ftof{
                                if (tempLay == 1){
                                    PFtof1aHitx[nmb] = tempX;
                                    PFtof1aHity[nmb] = tempY;
                                    PFtof1aHitz[nmb] = tempZ;
                                    PFtof1aTime[nmb] = tempTim;
                                    PFtof1aPath[nmb] = tempPat;
                                }
                                if (tempLay == 2){
                                    PFtof1bHitx[nmb] = tempX;
                                    PFtof1bHity[nmb] = tempY;
                                    PFtof1bHitz[nmb] = tempZ;
                                    PFtof1bTime[nmb] = tempTim;
                                    PFtof1bPath[nmb] = tempPat;
                                }
                                if (tempLay == 3){
                                    PFtof2Hitx[nmb] = tempX;
                                    PFtof2Hity[nmb] = tempY;
                                    PFtof2Hitz[nmb] = tempZ;
                                    PFtof2Time[nmb] = tempTim;
                                    PFtof2Path[nmb] = tempPat;
                                }
                            }

                            if (tempDet == 4 ){// ctof{
                                PCtofHitx[nmb] = tempX;
                                PCtofHity[nmb] = tempY;
                                PCtofHitz[nmb] = tempZ;
                                PCtofTime[nmb] = tempTim;
                                PCtofPath[nmb] = tempPat;
                            }
                        }
                    }//end of scintillators

                    // DC, CVT Bank (REC::Traj)        //
                    for(auto ipa2 = 0; ipa2<c12.getBank(idx_Traj)->getRows();ipa2++){

                        auto tempPnd_Traj = c12.getBank(idx_Traj)->getInt(iPindex,ipa2);
                        auto tempDet_Traj = c12.getBank(idx_Traj)->getInt(iDetector,ipa2);    
                        auto tempLay_Traj = c12.getBank(idx_Traj)->getInt(iLayer,ipa2); 
                        auto tempX_Traj = c12.getBank(idx_Traj)->getFloat(iX,ipa2); 
                        auto tempY_Traj = c12.getBank(idx_Traj)->getFloat(iY,ipa2); 
                        auto tempZ_Traj = c12.getBank(idx_Traj)->getFloat(iZ,ipa2);

                        if (tempPnd_Traj == Before[ipa]){
                            if (tempDet_Traj == 6 ){// dc
                                if (tempLay_Traj == 6){ //r1
                                    PDc1Hitx[nmb] = tempX_Traj;
                                    PDc1Hity[nmb] = tempY_Traj;
                                    PDc1Hitz[nmb] = tempZ_Traj;
                                }

                                if (tempLay_Traj == 18){ //r2
                                    PDc2Hitx[nmb] = tempX_Traj;
                                    PDc2Hity[nmb] = tempY_Traj;
                                    PDc2Hitz[nmb] = tempZ_Traj;
                                }

                                if (tempLay_Traj == 36){ //r3
                                    PDc3Hitx[nmb] = tempX_Traj;
                                    PDc3Hity[nmb] = tempY_Traj;
                                    PDc3Hitz[nmb] = tempZ_Traj;
                                }
                            }

                            if (tempDet_Traj == 5 ){// cvt
                                if (tempLay_Traj == 1){ //svt1
                                    PCvt1Hitx[nmb] = tempX_Traj;
                                    PCvt1Hity[nmb] = tempY_Traj;
                                    PCvt1Hitz[nmb] = tempZ_Traj;
                                }
                                if (tempLay_Traj == 3){ //svt3
                                    PCvt3Hitx[nmb] = tempX_Traj;
                                    PCvt3Hity[nmb] = tempY_Traj;
                                    PCvt3Hitz[nmb] = tempZ_Traj;
                                }
                                if (tempLay_Traj == 5){ //svt5
                                    PCvt5Hitx[nmb] = tempX_Traj;
                                    PCvt5Hity[nmb] = tempY_Traj;
                                    PCvt5Hitz[nmb] = tempZ_Traj;
                                }
                                if (tempLay_Traj == 7){ //bmt1
                                    PCvt7Hitx[nmb] = tempX_Traj;
                                    PCvt7Hity[nmb] = tempY_Traj;
                                    PCvt7Hitz[nmb] = tempZ_Traj;
                                }
                                if (tempLay_Traj == 12){ //bmt6
                                    PCvt12Hitx[nmb] = tempX_Traj;
                                    PCvt12Hity[nmb] = tempY_Traj;
                                    PCvt12Hitz[nmb] = tempZ_Traj;
                                }
                            }
                        }
                    }//end of REC::Traj

                    // REC::Track       //
                    for(auto ipa3 = 0; ipa3<c12.getBank(ldx_Track)->getRows();ipa3++){

                        auto tempPnd_Track = c12.getBank(ldx_Track)->getInt(lPindex,ipa3);
                        auto tempchi2_Track = c12.getBank(ldx_Track)->getFloat(lchi2,ipa3); 
                        auto tempNDF_Track = c12.getBank(ldx_Track)->getInt(lNDF,ipa3); 

                        if (tempPnd_Track == Before[ipa]){
                            Pchi2track[nmb] = tempchi2_Track;
                            PNDFtrack[nmb] = tempNDF_Track;
                        }
                    }//end of REC::Track
                
                    nmb++;
                } // end of protons
                        
                if((c12.getBank(idx_RECPart)->getInt(iPid,ipa)) == 22  ){  // photons

                    Gpx[nmg] = tPx;
                    Gpy[nmg] = tPy;
                    Gpz[nmg] = tPz;
                    Gstat[nmg] = tStat;
                    Gedep[nmg] = 0;
                    Gedep1[nmg] = 0;
                    Gedep2[nmg] = 0;
                    Gedep3[nmg] = 0;
                    GcX[nmg] = 0;
                    GcY[nmg] = 0;
                    Gtime[nmg] = 0;
                    Gpath[nmg] = 0;
                    if (Gstat[nmg]<2000) Gsector[nmg] = Gstat[nmg];
                    else Gsector[nmg] = PcalSector[ipa];

                    // EC Bank (REC::Calorimeter)        //
                    for(auto ipa2 = 0; ipa2<c12.getBank(mdx_Calo)->getRows();ipa2++){

                        auto tempPnd_Calo = c12.getBank(mdx_Calo)->getInt(mPindex,ipa2);
                        auto tempDet_Calo = c12.getBank(mdx_Calo)->getInt(mDetector,ipa2);    
                        auto tempLay_Calo = c12.getBank(mdx_Calo)->getInt(mLayer,ipa2); 
                        auto tempE_Calo = c12.getBank(mdx_Calo)->getFloat(menergy,ipa2); 
                        auto tempX_Calo = c12.getBank(mdx_Calo)->getFloat(mx,ipa2); 
                        auto tempY_Calo = c12.getBank(mdx_Calo)->getFloat(my,ipa2); 
                        auto tempTime_Calo = c12.getBank(mdx_Calo)->getFloat(mtime,ipa2); 
                        auto tempPath_Calo = c12.getBank(mdx_Calo)->getFloat(mpath,ipa2); 

                        if (tempPnd_Calo == Before[ipa]){
                            if (tempLay_Calo == 1) {
                                Gedep1[nmg] = tempE_Calo;
                                GcX[nmg] = tempX_Calo;
                                GcY[nmg] = tempY_Calo;
                                Gtime[nmg] = tempTime_Calo;
                                Gpath[nmg] = tempPath_Calo;
                            }
                            if (tempLay_Calo == 4) Gedep2[nmg] = tempE_Calo;
                            if (tempLay_Calo == 7) Gedep3[nmg] = tempE_Calo;
                            Gedep[nmg] += tempE_Calo;
                        }
                    } // end of EC bank

                    // FT Bank (REC::ForwardTagger)        //
                    for(auto ipa3 = 0; ipa3<c12.getBank(ndx_FT)->getRows();ipa3++){

                        auto tempPnd_FT = c12.getBank(ndx_FT)->getInt(nPindex,ipa3);
                        auto tempDet_FT = c12.getBank(ndx_FT)->getInt(nDetector,ipa3);    
                        auto tempLay_FT = c12.getBank(ndx_FT)->getInt(nLayer,ipa3); 
                        auto tempE_FT = c12.getBank(ndx_FT)->getFloat(nenergy,ipa3); 
                        auto tempX_FT = c12.getBank(ndx_FT)->getFloat(nx,ipa3); 
                        auto tempY_FT = c12.getBank(ndx_FT)->getFloat(ny,ipa3); 
                        auto tempTime_FT = c12.getBank(ndx_FT)->getFloat(ntime,ipa3); 
                        auto tempPath_FT = c12.getBank(ndx_FT)->getFloat(npath,ipa3); 

                        if (tempPnd_FT == Before[ipa]){
                            Gedep[nmg] = tempE_FT;
                            GcX[nmg] = tempX_FT;
                            GcY[nmg] = tempY_FT;
                            Gtime[nmg] = tempTime_FT;
                            Gpath[nmg] = tempPath_FT;
                        }
                    } // end of FT bank
                    nmg++;
                } //end of photons
            } //end of REC::Particle

            // event bank ====
            for(auto ipa1 = 0; ipa1<c12.getBank(idx_RECEv)->getRows();ipa1++){
                auto tempB = c12.getBank(idx_RECEv)->getFloat(aBeamQ,ipa1);
                auto tempL = c12.getBank(idx_RECEv)->getDouble(aLiveT,ipa1);
                auto tempS = c12.getBank(idx_RECEv)->getFloat(aStarT,ipa1);
                auto tempR = c12.getBank(idx_RECEv)->getFloat(aRFTim,ipa1);
                auto tempH = c12.getBank(idx_RECEv)->getInt(aHelic,ipa1);
                auto tempHR = c12.getBank(idx_RECEv)->getInt(aHeRaw,ipa1);

                beamQ = tempB;
                liveTime = tempL;
                startTime = tempS;
                RFTime = tempR;
                helicity = tempH;
                helicityRaw = tempHR;
            }

            bool condition = (nmb>0) && (nmg>0) && (nmG>0);
            if (mode == "pi0") condition = (nmb>0) && (nmg>1) && (nmG>0);
            if (mode == "ep") condition = (nmb>0);
            if (condition) T->Fill();
        }
    }

	rFile->Write();
	rFile->Close();

    return 1;
}
