#!/usr/bin/python3
# Copyright 2020 Aaron Webster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import datetime
import os
import astral
import astral.sun
import astral.geocoder
import configparser
import collections

from absl import app
from absl import logging

BASEDIR = '/tmp/onsun'


def main(argv):
  del argv  # unused
  config = configparser.ConfigParser()
  config_path = os.path.join(BASEDIR, 'config')
  with open(config_path) as f:
    config.read(config_path)

  city = astral.LocationInfo(
      name=config['DEFAULT']['name'],
      region=config['DEFAULT']['region'],
      timezone=config['DEFAULT']['region'],
      latitude=float(config['DEFAULT']['latitude']),
      longitude=float(config['DEFAULT']['longitude']))
  logging.info('Location: %s', city)

  epochs = astral.sun.sun(city.observer, date=datetime.date.today())
  for name, epoch in epochs.items():
    exec_dir = os.path.join(BASEDIR, '%s.d' % name)
    if not os.path.exists(exec_dir):
      continue

    for exec_path in os.listdir(exec_dir):
      # Get full path and resolve symbolic links.
      exec_path = os.path.realpath(os.path.join(exec_dir, exec_path))
      if not os.access(exec_path, os.X_OK):
        logging.fatal('%s is not executable.', exec_path)

      # Apply offset from the config, if specified.
      offset_hours = 0
      offset_minutes = 0
      offset_spec = config.get(
          os.path.basename(exec_path), name + '_offset', fallback=None)
      if offset_spec is not None:
        offset_hours, offset_minutes = offset_spec.split(':')
        logging.info('Applying %s offset of %s:%s to %s', name, offset_hours,
                     offset_minutes, exec_path)
        print(epoch)

      # Schedule only if the exec time is in the future.
      scheduled_exec = epoch - datetime.timedelta(
          hours=int(offset_hours), minutes=int(offset_minutes))
      if datetime.datetime.now(datetime.timezone.utc) < scheduled_exec:
        logging.info('%s will be run %s (%s)', exec_path,
                     scheduled_exec.astimezone(), name)
        os.system('/usr/bin/systemd-run --on-calendar="%s" %s' %
                  (scheduled_exec.strftime('%Y-%m-%d %H:%M:%S %Z'), exec_path))
      else:
        logging.warning(
            'Executition time for %s (%s, %s) is in the past, ignoring.',
            exec_path, scheduled_exec.astimezone(), name)


if __name__ == '__main__':
  app.run(main)
