# Raijin

Consulting service for the timezone of your electric rate 

### Installation

You can install from source with:

```
$ git clone https://github.com/ingran/raijin.git --recursive
$ cd raijin
$ pip install -r requirements.txt
```

### Configuration

#### Holidays

The file `holidays.json` in folder `config` contains the oficial holidays marked by [OMIE](http://www.omel.es/inicio/mercados-y-productos/mercado-electricidad/calendarios-y-periodos)

The structure of the file is one entry with the year as property name and array of 12 arrays. Each array represents one month and the values os the array of each month reprents a holiday. You can use `holidays_scheme.json` to create new holidays file for custom service.

#### Tariffs

The file `tariffs.json` in flder `config` contains the timezones of the different tariffs.

The structure of the file is one property with name ***tariffs***, wich contains an array of tariff objects.

You can use `tariffs_scheme.json` to create new tariffs file for custom service.
