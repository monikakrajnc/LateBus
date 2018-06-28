#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 19:33:43 2018

@author: monikakrajnc
"""

import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('Routelist1.py', 'Routelist2.py', 'Routelist3.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=3)                                                        
pool.map(run_process, processes) 
