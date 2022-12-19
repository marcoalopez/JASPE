# -*- coding: utf-8 -*-
# ============================================================================ #
#                                                                              #
#    JASPE script                                                              #
#    JASPE stands for Just Another Stereoplot in a Python Environment          #
#                                                                              #
#    Copyright (c) 2017-present   Marco A. Lopez-Sanchez                       #
#                                                                              #
#    This Source Code Form is subject to the terms of the Mozilla Public       #
#    License, v. 2.0. If a copy of the MPL was not distributed with this       #
#    file, You can obtain one at http://mozilla.org/MPL/2.0/.                  #
#                                                                              #
#    Covered Software is provided under this License on an “AS IS” BASIS,      #
#    WITHOUT WARRANTY OF ANY KIND, either expressed, implied, or statutory,    #
#    including, without limitation, warranties that the Covered Software is    #
#    FREE OF DEFECTS, merchantable, fit for a particular purpose or            #
#    non-infringing. The entire risk as to the quality and performance         #
#    of the Covered Software is with You. Should any Covered Software prove    #
#    defective in any respect, You (not any Contributor) assume the cost of    #
#    any necessary servicing, repair, or correction. This disclaimer of        #
#    warranty constitutes an essential part of this License. No use of any     #
#    Covered Software is authorized under this License except under this       #
#    disclaimer.                                                               #
#                                                                              #
#    Version alpha  0.3                                                        #
#    For details see: https://github.com/marcoalopez/JASPE                     #
#    download at https://github.com/marcoalopez/JASPE/releases                 #
#                                                                              #
#    Requirements:                                                             #
#        Python version 3.5 or higher                                          #
#        Numpy version 1.11 or higher                                          #
#        Matplotlib version 2.0 or higher                                      #
#        Pandas version x.x or higher                                          #
#                                                                              #
# ============================================================================ #

# Import some scientific libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Examples
# fig, ax = stereoplot()
# fig, (ax1, ax2) = stereoplot(nrows=1, ncols=2)
# fig, ((ax1, ax2), (ax3, ax4)) = stereoplot(nrows=2, ncols=2)

ax = None


def stereoplot(nrows=1, ncols=1):
    """Automatically generate a defined number of stereoplots using
    the matplotlib library

    Parameters
    ----------
    nrows : positive integer
        the number of rows of the subplot grid

    ncols : positive integer
        the number of columns of the subplot grid

    Call functions
    --------------
    set_stereo

    Return
    ------
    TODO
    """
    num_plots = nrows * ncols

    if num_plots == 1:
        fig, ax = plt.subplots()
        set_stereo(ax)
        fig.tight_layout()

        return fig, ax

    else:
        if nrows == 1:
            fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharey=True)
        elif ncols == 1:
            fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True)
        else:
            fig, ax = plt.subplots(nrows=nrows, ncols=ncols)

        for item in fig.axes:
            set_stereo(item)

        fig.tight_layout()

        return fig, fig.axes


def set_stereo(ax):
    """Tweak the matplotlib figure axes to plot a stereographic projection of
    unit radius.

    Parameters
    ----------
    ax : a matplotlib object
        the axes
    """

    # draw the contour and the centre of the circle
    ax.plot(0, 0, 'k+')
    circ = plt.Circle((0, 0), 1.0, facecolor='none', edgecolor='black')
    ax.add_patch(circ)

    # draw basic plot elements (ticks, reference)
    # TODO

    # draw grids (optional)
    # TODO

    ax.set_axis_off()  # remove the box, ticks, etc.
    ax.axis('equal')  # ensure equal aspect ratio

    return None


def plot_eq_area(azimuth, dip, axe=ax, **kwargs):
    """Plot the coordinates of a line in an equal area projection
    of unit radius.

    Parameters
    ----------
    azimuth : scalar or array_like with values between 0 and 360
        angle between the north vector and the line on the horizontal
        plane in spherical coordinates (0 - 360 degrees)

    dip : scalar or array_like with values between 0 and 90
        plunge or dip of line (0 - 90 degrees)

    axe : object, ax by default
        the figure axe

    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls),
        norm, cmap, transform, etc.

    Examples
    --------
    >>> plot_eq_area(180, 45)
    >>> plot_eq_area(270, 45, marker='h', color='green', markersize=12)

    Call function(s)
    --------------
    - sph_to_eq_area
    """

    x, y = sph_to_eq_area(azimuth, dip)

    return axe.plot(x, y, 'o', **kwargs)


def plot_eq_angle(azimuth, dip, axe=ax, **kwargs):
    """Plot the coordinates of a line in an equal angle projection
    of unit radius.

    Parameters
    ----------
    azimuth : scalar or array_like with values between 0 and 360
        angle between the north vector and the line on the horizontal
        plane in spherical coordinates (0 - 360 degrees)

    dip : scalar or array_like with values between 0 and 90
        plunge or dip of line (0 - 90 degrees)

    axe : object, ax by default
        the figure axe

    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls),
        norm, cmap, transform, etc.

    Examples
    --------
    >>> plot_eq_angle(180, 45)
    >>> plot_eq_angle(270, 45, marker='h', color='blue', markersize=12)

    Call function(s)
    --------------
    - sph_to_eq_angle
    """

    x, y = sph_to_eq_angle(azimuth, dip)

    return axe.plot(x, y, 'o', **kwargs)


def sph_to_eq_area(azimuth, dip):
    """Calculate the spherical coordinates of a line in an equal area stereographic
    projection of unit radius

    Parameters
    ----------
    azimuth : scalar or array_like with values between 0 and 360
        angle between the north vector and the line on the horizontal
        plane in spherical coordinates (0 - 360 degrees)

    dip : scalar or array_like with values between 0 and 90
        plunge or dip of line in spherical coordinates (degrees)

    Returns
    -------
    a float or numpy array with the stereographic equal-area coordinates (x, y)
    """

    # convert degrees to radians
    azimuth = np.deg2rad(azimuth)
    dip = np.deg2rad(dip)

    x = np.sqrt(2) * np.sin((np.pi / 4.0) - (dip / 2)) * np.sin(azimuth)
    y = np.sqrt(2) * np.sin((np.pi / 4.0) - (dip / 2)) * np.cos(azimuth)

    return x, y


def sph_to_eq_angle(azimuth, dip):
    """Calculate the spherical coordinates of a line in an equal angle
    stereographic projection of unit radius

    Parameters
    ----------
    azimuth : scalar or array_like with values between 0 and 360
        angle between the north vector and the line on the horizontal
        plane in spherical coordinates (0 - 360 degrees)

    dip : scalar or array_like with values between 0 and 90
        plunge or dip of line in spherical coordinates (degrees)

    Returns
    -------
    a float or numpy array with the coordinates (x, y)
    """

    # convert degrees to radians
    azimuth = np.deg2rad(azimuth)
    dip = np.deg2rad(dip)

    x = np.tan((np.pi / 4.0) - (dip / 2)) * np.sin(azimuth)
    y = np.tan((np.pi / 4.0) - (dip / 2)) * np.cos(azimuth)

    return x, y


def sph_to_cart(azimuth, dip, plot3D=False):
    """Convert from spherical (azimuth, dip) to cartesian coordinates.
    It returns the north, east, and down direction cosines of a line.

    Parameters
    ----------
    azimuth : scalar or array_like with values between 0 and 360
        angle between the north vector and the line on the horizontal
        plane in spherical coordinates (0 - 360 degrees)

    dip : scalar or array_like with values between 0 and 90
        plunge or dip of line in spherical coordinates (degrees)

    Returns
    -------
    a numpy array with the direction cosines (north, east, down)
    """

    # convert degrees to radians
    azimuth = np.deg2rad(azimuth)
    dip = np.deg2rad(dip)

    # estimate direction cosines
    east_cos = np.cos(dip) * np.sin(azimuth)
    north_cos = np.cos(dip) * np.cos(azimuth)
    down_cos = np.sin(dip)

    if plot3D is True:
        from mpl_toolkits.mplot3d import Axes3D
        figura = plt.figure()
        ax3d = figura.add_subplot(111, projection=Axes3D.name)
        ax3d.scatter(xs=north_cos, ys=east_cos, zs=down_cos, zdir='z')

    return north_cos, east_cos, down_cos


def cart_to_sph(north_cos, east_cos, down_cos):
    """Convert from cartesian to spherical coordinates and returns the
    azimuth and the plunge of a line.

    Parameters
    ----------
    north_cos : scalar or array-like
        north direction cosine

    east_cos : scalar or array-like
        east direction cosine

    down_cos : scalar or array-like
        down direction cosine

    Call function
    -------------
    - zero_to_pi

    Returns
    -------
    a numpy array with spherical coordinates (azimuth, dip)
    """

    # calculate dip
    dip = np.arcsin(down_cos)

    # calculate azimuth
    if north_cos == 0.0:  # north direction cosine zero case
        if east_cos < 0.0:
            azimuth = (3 / 2) * np.pi  # azimuth is West
        else:
            azimuth = (1 / 2) * np.pi  # azimuth is East

    else:
        azimuth = np.arctan(east_cos / north_cos)

        if north_cos < 0.0:
            azimuth = azimuth + np.pi

        # Check whether azimuth lies between 0 and 2*pi radians
        azimuth = zero_to_pi(azimuth)

    # convert radians to degrees
    azimuth = np.rad2deg(azimuth)
    dip = np.rad2deg(dip)

    return azimuth, dip


def mean_vector(azimuth, dip, conf=95):
    """Estimate the mean vector for a given set of vectors.

    Parameters
    ----------
    azimuth : scalar or array-like with values between 0 and 360
        line direction (azimuth) in spherical coordinates (degrees)

    plunge : scalar or array_like with values between 0 and 90
        plunge or dip of line in spherical coordinates (degrees)

    conf : integer or float between 0 and 100
        the cone level of confidence (default 95 %)

    Call functions
    --------------
    - sph_to_cart
    - cart_to_sph

    Returns
    -------
    mean azimuth and dip
    """

    n = len(azimuth)

    # sum the different cosine directions
    Nc, Ec, dc = sph_to_cart(azimuth, dip)
    Nc_sum, Ec_sum, dc_sum = np.sum(Nc), np.sum(Ec), np.sum(dc)

    # Estimate the resultant vector (R)
    R = np.sqrt(Nc_sum**2 + Ec_sum**2 + dc_sum**2)
    rave = R / n  # normalize to n

    # check significance
    if rave < 0.1:
        print('Mean vector is insignificant')
    else:
        Nc_sum, Ec_sum, dc_sum = Nc_sum / R, Ec_sum / R, dc_sum / R

    # convert mean vector to lower hemisphere
    if dc_sum < 0.0:
        Nc_sum, Ec_sum, dc_sum = -Nc_sum, -Ec_sum, -dc_sum

    # convert direction cosines to spherical coordinates (azimuth and dip)
    azimuth, dip = cart_to_sph(Nc_sum, Ec_sum, dc_sum)

    # Estimate statistics based on Fisher et al. (1987)
    # Concentration factor
    if R < n:
        if n < 16:
            afact = 1.0 - (1.0 / n)
            conc = (n / (n - R)) * afact**2
        else:
            conc = (n - 1.0) / (n - R)

    # estimate uncertainty cones
    if rave >= 0.65 and rave < 1.0:
        bfact = 1.0 / (n - 1.0)
        afact = 1.0 / (1.0 - conf)
        d = np.arccos(1.0 - ((n - R) / R) * (afact**(bfact - 1.0)))

    print('Mean vector = {a}/{b} azimuth/dip' .format(a=azimuth, b=dip))
    print('Fisher statistics:')
    print('concentration factor =', conc)
    print('uncertainty cone = {a} at {b} % level of confidence' .format(a=d, b=conf))

    return azimuth, dip


def zero_to_pi(azimuth):
    """Constrains azimuth between 0 and 2*pi radians

    Parameter
    ---------
    azimuth : float
        the azimuth in radians
    """

    if azimuth < 0.0:
        azimuth = azimuth + (2 * np.pi)
    else:
        azimuth = azimuth - (2 * np.pi)

    return azimuth


def import_data(file_path='auto', delimiter=None, skiprows=None):
    """ Extract the data from tabular-like files

    Parameters
    ----------
    file_path : string
        The file location in the OS in quotes
        e.g: 'C:/...yourFileLocation.../nameOfTheFile.csv'
        If 'auto' (the default) the function will ask you for the location of
        the file through a file selection dialog.

    delimiter : string, default: None
        Delimiter to use. The pandas method try to automatically detect the
        separator, but it can be defined by the user.

    skiprows : integer, list-like or callable. Default: None
        Line numbers to skip (0-indexed) or number of lines to skip (int) at the
        start of the text file.

    Returns
    -------
    A pandas dataframe (tabular data) with all the data contained in the text file
    plus a quick view of the data imported (in the console)
    """

    if file_path == 'auto':
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select file",
                                               filetypes=[('Text files', '*.txt'),
                                               ('Text files', '*.csv')])

    # check the extension of the file
    if file_path.endswith('.txt'):
        data_frame = pd.read_table(file_path, delimiter=delimiter, skiprows=skiprows)

    elif file_path.endswith('.csv'):
        data_frame = pd.read_csv(file_path, delimiter=delimiter, skiprows=skiprows)

    else:
        print("Error: The file is not a 'txt' nor 'csv' or the file extension was not specified.")
        return None

    print(' ')
    print(data_frame.head())
    print('...')
    print(data_frame.tail())
    print(' ')

    return data_frame


def plot_projection(ax, form='area'):
    """Plot a text indicating whether the projection is equal-area
    or equal-angle

    Parameters
    ----------
    ax :
        the Matplotlib axe

    form : string
        'area' for equal-area, 'angle' for equal-angle
    """

    if form == 'area':
        ax.text(-1, -1, 'Equal area projection \n Lower hemisphere',
                horizontalalignment='center')
        return None

    elif form == 'angle':
        ax.text(-1, -1, 'Equal angle projection \n Lower hemisphere',
                horizontalalignment='center')
        return None

    else:
        print("Wrong form. Please use 'area' or 'angle'")
        return None
