#!/usr/bin/env python
'''
           _/  _/   
╔═╗╦ ╦╦   _/  _/    ╔╦╗╔═╗╔╗ ╔═╗╔═╗
║ ╦║ ║║  _/_/_/_/   ║║║║ ║╠╩╗╚═╗║╣   
╚═╝╚═╝╩     _/      ╩ ╩╚═╝╚═╝╚═╝╚═╝
           _/

Graphic Interface to evolve single system with MOBSE (by using the public version).
It's based on PySimpleGUI (https://pypi.org/project/PySimpleGUI/).
Author: N. Giacobbo
Year: Jan 2021
'''
# Modules for setting the GUI 
import PySimpleGUI as sg
import base64
import os.path
print(sg) # useful to check what PySimpleGUI you are using
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib
matplotlib.use('TkAgg')
import PIL
# Modules for showing the logo in the window
from PIL import Image, ImageTk
import io
# Modules to compile and run MOBSE
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
import fileinput # to replace string in a file
import sys
import subprocess # to run bash commands 
import pandas

# ----------------------------------- Beginning of the setting funs ------------------------
def replace_input(element, value, file):
    '''
    Replace the element's value contained in file
    '''
    print(value,element)
    for line in fileinput.input(file, inplace=True):
        if line.strip().startswith(element):
            # the the space at the beginning are necessary in Fortran
            line = '      ' + element + ' = ' + str(value) + '\n' 
        sys.stdout.write(line)

def compile_and_run(compile=False):
    # Check the prence of the mobse's folder
    if not os.path.exists('mobse'):
            print('Warning: you have to download MOBSE!')
            #subprocess.run(['python','tools/download.py']) 
    subprocess.run(['make','clean'])
    subprocess.run(['make','mobseGUI'])
    subprocess.run(['./mobseGUI.x'])

def plot_mass_evolution(filename='output/mobse_long.out'):
    fig = matplotlib.figure.Figure(figsize=(8, 7), dpi=200)
    data = pandas.read_csv(filename, delimiter='\s+', header=0)
    ax = fig.add_subplot(111)
    ax.plot(data['time'], data['m1'], lw=2, c='forestgreen', label='$M_1$')
    ax.plot(data['time'], data['m2'], lw=2, c='deepskyblue', label='$M_2$')
    ax.set_xlabel('$t$ [Myr]')
    ax.set_ylabel('$m$ [M$_\odot$]')
    ax.set_xscale('log')
    # right y-axis
    axr = ax.twinx()
    axr.plot(data['time'], data['sep'], ls='--', lw=1.5, c='k', label='separation')
    axr.plot(data['time'], data['logR1'], ls='--', lw=1, c='forestgreen', label='$R_1$')    
    axr.plot(data['time'], data['logR2'], ls='--', lw=1, c='deepskyblue', label='$R_2$')
    axr.set_ylabel('[R$_\odot$]')
    axr.set_yscale('log')
    ax.legend(loc='upper right',frameon=False)
    axr.legend(loc='upper center', frameon=False)
    #print(data.columns)
    return fig
# ------------------------------ Beginning of Matplotlib helper codes ----------------------
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_graph(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')

# From a demo in the PySimpleGUI'repo
def figure_to_image(figure):
    '''
    Draws the previously created "figure" in the supplied Image Element
    :param element: an Image Element
    :param figure: a Matplotlib figure
    :return: The figure canvas
    '''
    plt.close('all')        # erases previously drawn plots
    canv = FigureCanvasAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    return buf.read()

# From a demo in the PySimpleGUI'repo
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

# ------------------------------------ Beginning of GUI code -------------------------------
# Define the MyNewTheme
sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND': '#F48810',
                                        'TEXT': '#FFFFFF',
                                        'INPUT': '#F7E700',
                                        'TEXT_INPUT': '#000000',
                                        'SCROLL': '#c7e78b',
                                        'BUTTON': ('white', '#F43410'),
                                        'PROGRESS': ('#01826B', '#D0D0D0'),
                                        'BORDER': 2, 'SLIDER_DEPTH': 1, 'PROGRESS_DEPTH': 1,
                                        }
# Switch to use your newly created theme
sg.theme('MyNewTheme')

# Transform png in base64. It will appear as logo of the app
with open("pics/logo_mobse.png", "rb") as img:
    my_icon = base64.b64encode(img.read())
sg.SetOptions(icon=my_icon)

# Transform png in base64. It will appear as logo in the app
with open("pics/logo_mobse_small.png", "rb") as img:
    my_icon_small = img.read()

# Set first column: INPUTS 
column_inputs = [
    [sg.Text('', size=(7,1)), sg.Image(data=my_icon_small, key='__IMAGE__', size=(120, 100))],
    [sg.Text('_'  * 130, size=(30, 1))],
    [sg.Text('Initial conditions:', justification='center', font=('Arial', 16), size=(20, 1))],  
    [sg.Text('M1 [Msun] =', size=(10, 1)), sg.Input(key='m1', default_text=20., size=(10,1))],
    [sg.Text('M2 [Msun] =', size=(10, 1)), sg.Input(key='m2', default_text=10., size=(10,1))],
    [sg.Text('ecc =', size=(10, 1)), sg.Input(key='ecc', default_text=0.1, size=(10,1))],
    [sg.Text('P [day] =', size=(10, 1)), sg.Input(key='tb', default_text=1000., size=(10,1))],
    [sg.Text('Z =', size=(10, 1)), sg.Input(key='z', default_text=0.02, size=(10,1))],
    [sg.Text('_'  * 130, size=(30, 1))],
    [sg.Text('Parameters:', justification='center', font=('Arial', 16), size=(20, 1))],
    [sg.Text('alpha =', size=(10, 1)), sg.Input(key='alpha1', default_text=5., size=(10,1))],
    [sg.Text('lambda =', size=(10, 1)), sg.Input(key='lambda', default_text=0.1, size=(10,1))],
    [sg.Text('SN =', size=(10, 1)), sg.Input(key='nsflag', default_text=3, size=(10,1))],
    [sg.Text('kick =', size=(10, 1)), sg.Input(key='bhflag', default_text=3., size=(10,1))],
    [sg.Text('_'  * 100, size=(25, 1))],
    [sg.Button('Update'), sg.Button('Run'), sg.Button('Plot'), sg.Button('Exit')]
]
# Set second column: PLOTS 
column_plots = [
    [sg.Image(k=(0,0))]
]
# define figure size
figure_w, figure_h = 520, 520

# Full layout
layout = [[sg.Column(column_inputs), sg.VSeparator(), sg.Column(column_plots)]]

# Create window and show it without the plot
window = sg.Window('Evolve sinlge binaries with MOBSE', layout)

# List of input and parameters
params = ['alpha1','lambda','nsflag','bhflag']
ini_conds = ['m1','m2','ecc','tb','z']

while True:  # Event Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Update':
        # Update input files
        for i in ini_conds:
            print(values[i])
            replace_input(i, values[i], 'input/binary.h')
        for i in params:
            print(values[i])
            replace_input(i,values[i], 'input/parameters.h')
    elif event == 'Run':
        # Run MOBSE
        compile_and_run()
    if event == 'Plot':
            fig = plot_mass_evolution()
            image = figure_to_image(fig)
            image = convert_to_bytes(image, (figure_w, figure_h))
            window[(0,0)].update(data=image)
#    if event == 'Plot':
# Plot the mass evolution from mobse.out
window.close()