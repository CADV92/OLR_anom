import xarray as xr

# Abrir el archivo NetCDF
ds_olr = xr.open_dataset("/home/spm/Downloads/olr.day.mean.nc")

# Seleccionar solo los años entre 1991 y 2020
ds_olr_climatologia = ds_olr.sel(time=slice("1991", "2020"))

# Calcular la climatología
climatologia = ds_olr_climatologia.groupby("time.dayofyear").mean(dim="time")

# Calcular las anomalías restando la climatología de los valores diarios
anomalias = ds_olr.groupby("time.dayofyear") - climatologia

# Crear un nuevo dataset solo con la variable de anomalía y renombrarla como "anom"
ds_anomalias = xr.Dataset({"anom": anomalias["olr"]})
ds_anomalias["anom"].attrs = ds_olr["olr"].attrs

ds_anomalias = ds_anomalias.drop_vars("dayofyear")

# Guardar los valores de OLR y anomalía en un archivo NetCDF
ds_combined = xr.Dataset({"olr": ds_olr["olr"], "anom": ds_anomalias["anom"]})
# ds_combined = ds_combined.drop_vars("dayofyear")
ds_combined.to_netcdf("./olr.nc")
