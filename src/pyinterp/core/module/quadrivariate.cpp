// Copyright (c) 2019 CNES
//
// All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.
#include <pybind11/pybind11.h>
#include "pyinterp/quadrivariate.hpp"

namespace py = pybind11;
namespace geometry = pyinterp::detail::geometry;

void init_quadrivariate(py::module& m) {
  pyinterp::implement_quadrivariate<geometry::EquatorialPoint4D, double,
                                    double>(m, "Float64");
  pyinterp::implement_quadrivariate<geometry::EquatorialPoint4D, double, float>(
      m, "Float32");
}
