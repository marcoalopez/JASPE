# JASPE

**JASPE** stands for **J**ust **A**nother **S**tereoplot **P**ython **E**nvironment. This is a pet project that I develop at my own pace and according to my needs and preferences. The script is therefore not primarily intended for general use but my own. You should not expect updates, new features, or bug fixes in reasonable times. Nor can I assure you that the project will be abandoned for a large period of time. My main goal with this is to include stereographic/equal-area projections in my Python work flow while interacting with standard Python scientific libraries. If you are looking for a software specifically dedicated to this there are better options out there, for example [here](http://www.geo.cornell.edu/geology/faculty/RWA/programs/stereonet.html), [here](http://www.frederickvollmer.com/orient/), or [here](http://www.igc.usp.br/index.php?id=openstereo). In any case, if you decide to use it or want to access the source code out of curiosity, do so at your own risk and responsibility downloading the script [here](https://github.com/marcoalopez/JASPE/releases). You can also fork the project on GitHub since it is free and open-source.

So far, the script only performs very basic tasks. One function tweaks the default features of matplotlib plots (i.e. the  standard Python plotting library) to generate single or multiple stereoplots, another is for importing tabular-like data, and the rest to transform between different reference frames; from spherical to equal area or equal angle stereographic coordinates or from spherical to cartesian coordinates and vice versa.

## Quick examples

```python
# Create a simple figure
fig, ax = plt.subplots()

# set the ...
set_stereo(ax)  # set the stereo
fig.tight_layout()  # assure a tight layout

# Plot some data using the function plot_data
plot_data(180, 45, ax)  # by default this is an equal-area projection
plot_data(180, 45, ax, form='angle')  # plot in equal-angle projection


# Create a figure with two stereos using matplotlib [oo] syntax
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)

# set the axes of the figures to...
set_stereo(ax1)
set_stereo(ax2)
fig.tight_layout()

# plot linear data in the first stereo (ax1)
azimuths = [0, 45, 90, 135, 180, 225, 270, 315, 360]
dips = [0, 10, 20, 30, 40, 50, 70, 80, 90]
plot_data(azimuths, dips, ax1)

# plot linear data from a txt file in the second stereo (ax2)

## first, import tabular-like data from text files. The function will ask you for
## the location of the file through a file selection dialog
dataset = import_data()  

Trend  Plunge Type
0    5.0    67.0    C
1    9.0     9.0    C
2   22.0    64.0    C
3   27.0    16.0    C
4   27.0    52.0    C
...
  Trend  Plunge Type
107  331.0    81.0    C
108  340.0    63.0    C
109  345.0    16.0    C
110  352.0    26.0    C
111  355.0    24.0    C

## This time we will use matplotlib syntax instead of using the plot_data funtion
## (this is the way to go if you want to control the figure aesthetics)

### Transform from spherical coordinates to equal-area coordinates
azimuths, dips = sph_to_eq_area(dataset['Trend'], dataset['Plunge'])

### Second, plot using matplotlib syntax
ax2.plot(azimuths, dips, 'h', color='C3', markersize=9, label='Kamb (1959) data')
```
