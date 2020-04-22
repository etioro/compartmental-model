
import pandas as pd
from math import floor, ceil, exp
from initialise_parameters import params, parameter_csv # , preparePopulationFrame, control_data
import numpy as np
import plotly.graph_objects as go
from functions import simulator, simulate_range_of_R0s, object_dump, generate_csv
from plotter import categories, figure_generator, age_structure_plot, stacked_bar_plot
from config import control_type, camp, timings, population_frame, population
import pickle
import os
cwd = os.getcwd()

##----------------------------------------------------------------
# load a saved solution?
load = True
# save generated solution? Only generates new if not loading old
# saves as a python pickle object
save = True
save_csv = True

##----------------------------------------------------------------
solution_name   = 'Solution_%s_%s_%s_%s'    %(camp,timings[0],timings[1],control_type)
percentile_name = 'Percentiles_%s_%s_%s_%s' %(camp,timings[0],timings[1],control_type)  

already_exists_soln       = os.path.isfile(os.path.join(cwd,'saved_runs/' + solution_name))
already_exists_percentile = os.path.isfile(os.path.join(cwd,'saved_runs/' + percentile_name))



if not load or not (already_exists_soln and already_exists_percentile): # generate solution if not wanting to load, or if wanting to load but at least one file missing
    # run model - change inputs via 'config.py'
    sols, percentiles =simulate_range_of_R0s(control_type, timings, population_frame, population) # returns solution for middle R0 and then minimum and maximum values by scanning across a range defined by low and high R0
    if save:
        object_dump('saved_runs/' + solution_name  ,  sols)
        object_dump('saved_runs/' + percentile_name,  percentiles)
else:
    sols        = pickle.load(open('saved_runs/' + solution_name, 'rb'))
    percentiles = pickle.load(open('saved_runs/' + percentile_name, 'rb'))


# example of generating csv (currently for middle R0 value)
# might also want to do save specific percentiles
# might want to include all age structure info (as currently is)
# or might want to just sum over all age classes to get a total
if save_csv:
    generate_csv(sols,population_frame,'middle_R0_'+solution_name)

## ----------------------------------------------------------------------------------------
# plots - change outputs via these below
multiple_categories_to_plot    = ['A','I','D'] # categories to plot
single_category_to_plot        = 'H'           # categories to plot in final 3 plots

no_control = False
if control_type=='No control':
    no_control = True

# plot graphs
fig1   = go.Figure(  figure_generator(sols,multiple_categories_to_plot,population,population_frame,timings,no_control))   # plot with lots of lines
fig2   = go.Figure(age_structure_plot(sols,single_category_to_plot,    population,population_frame,timings,no_control))   # age structure
fig3   = go.Figure(  stacked_bar_plot(sols,single_category_to_plot,    population,population_frame))                      # bar chart (age structure)
figU   = go.Figure(  figure_generator(sols,single_category_to_plot,    population,population_frame,timings,no_control,percentiles)) # uncertainty


# view
fig1.show()
fig2.show()
fig3.show()
figU.show()


# save
fig1.write_image("Figs/Disease_progress_%s.png" % camp)
fig2.write_image("Figs/Age_structure_%s_%s.png" %(camp,categories[single_category_to_plot]['longname']))
fig3.write_image("Figs/Age_structure_(bar_chart)_%s_%s.png" %(camp,categories[single_category_to_plot]['longname']))
figU.write_image("Figs/Uncertainty_%s_%s.png" %(camp,categories[single_category_to_plot]['longname']))