// Copyright (c) 2019 CNES
//
// All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.
#include <pybind11/pybind11.h>
#include "pyinterp/grid.hpp"

namespace py = pybind11;

void init_grid(py::module& m) {
  pyinterp::implement_grid<double>(m, "Float64");
  pyinterp::implement_grid<float>(m, "Float32");
}
