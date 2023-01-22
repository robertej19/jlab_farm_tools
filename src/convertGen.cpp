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

    TFile *rFile = TFile::Open("genOnly.root","RECREATE");
    TTree *T=new TTree("T","Gen");

   // =====  proton =====
    Float_t GenPpx;
    Float_t GenPpy;
    Float_t GenPpz;

    // ==== electron =====
    Float_t GenEpx;
    Float_t GenEpy;
    Float_t GenEpz;

    // ==== pi0s =====
    Float_t GenPipx;
    Float_t GenPipy;
    Float_t GenPipz; 
    
    // ==== gammas =====
    Int_t nmG;
    Float_t GenGpx[2];
    Float_t GenGpy[2];
    Float_t GenGpz[2];

// ===============    Electrons ==============    
    T->Branch("GenEpx",&GenEpx,"GenEpx/F");
    T->Branch("GenEpy",&GenEpy,"GenEpy/F");
    T->Branch("GenEpz",&GenEpz,"GenEpz/F");

// ===============    Protons ================================== 
    T->Branch("GenPpx",&GenPpx,"GenPpx/F");
    T->Branch("GenPpy",&GenPpy,"GenPpy/F");
    T->Branch("GenPpz",&GenPpz,"GenPpz/F");


// ===============    Pi0s ==================================
    T->Branch("GenPipx",&GenPipx,"GenPipx/F");
    T->Branch("GenPipy",&GenPipy,"GenPipy/F");
    T->Branch("GenPipz",&GenPipz,"GenPipz/F"); 


// ================   Gammas  ===============    
    T->Branch("nmG",&nmG,"nmG/I");
    T->Branch("GenGpx",&GenGpx,"GenGpx[nmG]/F");
    T->Branch("GenGpy",&GenGpy,"GenGpy[nmG]/F");
    T->Branch("GenGpz",&GenGpz,"GenGpz[nmG]/F");
    
  //
  //loop over files
  //
  for(int ifile=0; ifile<chain.GetNFiles();++ifile){
      clas12::clas12reader c12{chain.GetFileName(ifile).Data()};
      
      // MC particle bank ========
      auto idx_GenPart = c12.addBank("MC::Particle");
      auto iPid = c12.getBankOrder(idx_GenPart,"pid");
      auto iPx  = c12.getBankOrder(idx_GenPart,"px");
      auto iPy  = c12.getBankOrder(idx_GenPart,"py");
      auto iPz  = c12.getBankOrder(idx_GenPart,"pz");

        while(c12.next() == true){
    
          nmG=0;

          for(auto ipa=0;ipa<c12.getBank(idx_GenPart)->getRows();ipa++){
            
              auto tPx = c12.getBank(idx_GenPart)->getFloat(iPx,ipa);
              auto tPy = c12.getBank(idx_GenPart)->getFloat(iPy,ipa);
              auto tPz = c12.getBank(idx_GenPart)->getFloat(iPz,ipa);

              if( (c12.getBank(idx_GenPart)->getInt(iPid,ipa)) == 11  ){  // electrons
                  GenEpx = tPx;
                  GenEpy = tPy;
                  GenEpz = tPz;
              }
            
              if((c12.getBank(idx_GenPart)->getInt(iPid,ipa)) == 111  ){  // pi0s
                    GenPipx = tGenPx;
                    GenPipy = tGenPy;
                    GenPipz = tGenPz;
              }

              if((c12.getBank(idx_GenPart)->getInt(iPid,ipa)) == 2212  ){  // protons
                  GenPpx = tPx;
                  GenPpy = tPy;
                  GenPpz = tPz;
                                
              } // if for protons
              
                
              if((c12.getBank(idx_GenPart)->getInt(iPid,ipa)) == 22  ){  // photons
                  GenGpx[nmG] = tPx;
                  GenGpy[nmG] = tPy;
                  GenGpz[nmG] = tPz;
                  nmG++;
              }
          }

          if (nmG>0) T->Fill();

        }

    }

  rFile->Write();
  rFile->Close();

  return 1;
}