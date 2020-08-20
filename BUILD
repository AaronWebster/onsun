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

load("@rules_pkg//:pkg.bzl", "pkg_deb", "pkg_tar")

pkg_tar(
    name = "mode755_files",
    srcs = ["onsun.py"],
    mode = "0755",
    package_dir = "/etc/onsun/",
)

pkg_tar(
    name = "mode644_files",
    srcs = [
        "onsun.service",
        "onsun.timer",
    ],
    mode = "0644",
    package_dir = "/etc/systemd/system/",
)

pkg_tar(
    name = "debian_data",
    extension = "tar.gz",
    deps = [
        ":mode644_files",
        ":mode755_files",
    ],
)

pkg_deb(
    name = "onsun_deb",
    data = ":debian_data",
    description = "Runs sun-based events.",
    homepage = "https://github.com/AaronWebster/onsun",
    maintainer = "Aaron Webster",
    package = "onsun",
    postinst = "postinst",
    prerm = "prerm",
    version = "1.0.0",
)
