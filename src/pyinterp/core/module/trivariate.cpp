// Copyright (c) 2019 CNES
//
// All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.
#include <pybind11/pybind11.h>
#include "pyinterp/trivariate.hpp"

namespace py = pybind11;
namespace geometry = pyinterp::detail::geometry;

void init_trivariate(py::module& m) {
  pyinterp::implement_trivariate<geometry::EquatorialPoint3D, double, double,
                                 double>(m, "", "Float64");
  pyinterp::implement_trivariate<geometry::EquatorialPoint3D, double, double,
                                 float>(m, "", "Float32");

  pyinterp::implement_trivariate<geometry::TemporalEquatorial2D, double,
                                 int64_t, double>(m, "Temporal", "Float64");
}
