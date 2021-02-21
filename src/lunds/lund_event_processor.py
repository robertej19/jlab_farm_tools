#!/bin/python
#cython: language_level=3

import argparse
import sys
import os
import pickle


import numpy as np 
#import random 
#import sys
#import os, subprocess
import math


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def vec_angle(v1, v2):
    """stolen from https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249"""
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))*180/np.pi

def vec_subtract(vec1,vec2):
    res = tuple(map(lambda i, j: i - j, vec1, vec2)) 
    return res

def vec_add(vec1,vec2):
    res = tuple(map(lambda i, j: i + j, vec1, vec2)) 
    return res

def calc_inv_mass_squared(four_vector):
    fv = four_vector
    inv_mass2 = fv[0]**2-fv[1]**2-fv[2]**2-fv[3]**2
    return inv_mass2

def calculate_kinematics(event_frame):
    e_mass = 0.000511
    pro_mass = 0.938
    Ebeam_4mom = (10.6,0,0,10.6)

    #print("Event frame is:")
    #print(event_frame)
    photons = []
    for particle in event_frame:
        if particle[14] == 11:
            ele = particle
        if particle[14] == 2212:
            pro = particle
        if particle[14] == 22:
            photons.append(particle)
        
    

    # ele = event_df.query("particleID == 11")
    # pro = event_df.query("particleID == 2212")
    # photons = event_df.query("particleID == 22")

    #photon1 = photons.head(n=1)#This will only work for two photons!
    #photon2 = photons.tail(n=1)#This will only work for two photons!
   
    photon1 = photons[0]
    photon2 = photons[1]


    e_4mom =(ele[20],ele[17],ele[18],ele[19])
    pro_4mom = (pro[20],pro[17],pro[18],pro[19])
    pho1_4mom = (photon1[20],photon1[17],photon1[18],photon1[19])
    pho2_4mom = (photon2[20],photon2[17],photon2[18],photon2[19])


    # e_4mom = (ele["E_GeV"].values[0],ele["mom_x"].values[0],ele["mom_y"].values[0],ele["mom_z"].values[0])
    # pro_4mom = (pro["E_GeV"].values[0],pro["mom_x"].values[0],pro["mom_y"].values[0],pro["mom_z"].values[0])
    # pho1_4mom = (photon1["E_GeV"].values[0],photon1["mom_x"].values[0],photon1["mom_y"].values[0],photon1["mom_z"].values[0])
    # pho2_4mom = (photon2["E_GeV"].values[0],photon2["mom_x"].values[0],photon2["mom_y"].values[0],photon2["mom_z"].values[0])


    #e_energy = np.sqrt(e_mass**2+np.sum(np.square(e_mom)))

    target_4mom = (pro_mass,0,0,0)

    Eprime = e_4mom[0]

    virtual_gamma = vec_subtract(Ebeam_4mom,e_4mom)

    
    #Calculate kinematic quantities of interest
    Q2 = -1*calc_inv_mass_squared(virtual_gamma)
    nu = virtual_gamma[0]
    xB = Q2/(2*pro_mass*nu)

    pion_4mom = vec_add(pho1_4mom,pho2_4mom)

    #Calculate t
    #t = (P - P')^2
    #t[i] = 2*0.938*(p4_proton[i].E() - 0.938);
    t = -1*calc_inv_mass_squared(vec_subtract(target_4mom,pro_4mom)) 
    #Could also calculate this using (target+e_beam-e'-pion)

    #Calculate phi (trento angle)

    e3 = e_4mom[1:]
    v_lepton = np.cross(Ebeam_4mom[1:],e_4mom[1:])
    v_hadron = np.cross(pro_4mom[1:],virtual_gamma[1:])
    v_hadron2 = np.cross(pro_4mom[1:],pion_4mom[1:])

    phi = vec_angle(v_lepton,v_hadron)

    if (np.dot(v_lepton,pro_4mom[1:])>0):
        phi = 360 - phi
    



    return Q2, xB, t,phi,Eprime


    
def process_lund_into_events(df,run_num):
    events_list = []
    #num_events = df["event_num"].max()
    num_events = int(len(df)/4) #assuming there are 4 particles per event
    #print("Num events is {}".format(num_events))
    #sys.exit()
    for ind in range(0,num_events):
        if ind % 100 ==0:
            print("On event {}".format(ind))
        #event_dataframe = df.query("event_num == {}".format(ind))
        #event_dataframe = df[df["event_num"]==ind]
        #print(df)
        #evdnp = df.to_numpy()


        event_frame = []
        for row in df:
            if row[0]==ind:
                event_frame.append(row)
        #print(evdnp[0:5])
        

        event_num = ind
        lumi = 0
        heli = 0
        Ebeam = 10.6
        
        q2,xb,t,phi,Eprime = calculate_kinematics(event_frame)

        events_list.append([run_num,event_num,lumi,heli,
            Ebeam,Eprime,q2,xb,t,phi])
    
    return events_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    default_pkl_inname = "lund_simu_998.pkl"
    default_pandas_outname = "_evented.pkl"
    parser.add_argument("-i","--infile",help="Specify lund input filename",default=default_pkl_inname)
    parser.add_argument("-o","--outfile",help="Specify pandas outupt filename",default=default_pandas_outname)
    args = parser.parse_args()

    if not os.path.isfile(args.infile):
        print("Cannot find file {}, exiting".format(args.infile))
        sys.exit()

    if args.outfile == default_pandas_outname:
        args.outfile = args.infile.split(".")[0]+args.outfile
    
    out_labels = ["run","event","luminosity","helicity","Ebeam","Eprime","q2","xb","t","phi"]


    run_num = str(args.infile).split(".pkl")[0].split("_")[-1]
    


    #df = pd.read_pickle(args.infile)
    with open(args.infile, 'rb') as f:
        df = pickle.load(f)

    
    events_list = process_lund_into_events(df,run_num)

    #df_out = pd.DataFrame(events_list, columns=out_labels)
    #df_out.to_pickle(args.outfile)

    with open(args.outfile, 'wb') as f:
        pickle.dump(events_list, f)




        
        