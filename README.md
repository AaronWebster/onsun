# ONSUN

Runs programs on solar events.

## Installation.

First, install dependencies using:

```shell
  sudo pip3 install absl-py
  sudo pip3 install astral
```

Then, build and install the package:
```shell
  git clone https://github.com/AaronWebster/onsun.git
  cd onsun
  bazel build :onsun_deb
  sudo dpkg -i bazel-bin/onsun_1.0.0_all.deb
```

## Configuration.
Place the binaries/scripts you want to run in e.g. `/etc/solar/sunrise.d/` and
`/etc/solar/dusk.d/`.  Modify the configuration in `/etc/onsun/config` as
needed, for example.

```
[DEFAULT]
name = Eugene
region = Cascadia
timezone = America/Los_Angeles
latitude = 43.0521
longitude = -123.0868

[some_script]
sunrise_offset = 3:00
```

Valid epochs are `dawn`, `sunrise`, `noon`, `sunset`, and `dusk`.
