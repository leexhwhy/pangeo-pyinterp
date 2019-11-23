# Copyright (c) 2019 CNES
#
# All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
import os
import pickle
import unittest
import netCDF4
try:
    import matplotlib.pyplot
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False
import numpy as np
import pyinterp.core as core


def plot(x, y, z, filename):
    figure = matplotlib.pyplot.figure(figsize=(15, 15), dpi=150)
    value = z.mean()
    std = z.std()
    normalize = matplotlib.colors.Normalize(vmin=value - 3 * std,
                                            vmax=value + 3 * std)
    axe = figure.add_subplot(2, 1, 1)
    axe.pcolormesh(x, y, z, cmap='jet', norm=normalize)
    figure.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                filename),
                   bbox_inches='tight',
                   pad_inches=0.4)


class TestRTree(unittest.TestCase):
    """Test of the C+++/Python interface of the pyinterp::RTree class"""
    GRID = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "dataset", "mss.nc")

    @classmethod
    def load_data(cls, packing=True):
        """Creating the search tree"""
        with netCDF4.Dataset(cls.GRID) as ds:
            z = ds.variables['mss'][:].T
            z[z.mask] = float("nan")
            x = ds.variables['lon'][:]
            y = ds.variables['lat'][:]
            # Since insertion is slower, the data are sub-sampled to avoid
            # the test being too long.
            if not packing:
                x = x[::5]
                y = y[::5]
                z = z[::5, ::5]
            x = x.astype("float32")
            y = y.astype("float32")
            z = z.astype("float32")
            x, y = np.meshgrid(x, y, indexing='ij')
            mesh = core.RTreeFloat32(core.geodetic.System())
            if packing:
                mesh.packing(
                    np.vstack((x.flatten(), y.flatten())).T, z.data.flatten())
            else:
                mesh.insert(
                    np.vstack((x.flatten(), y.flatten())).T, z.data.flatten())
            return mesh

    def test_rtree_interpolate(self):
        """Interpolation test"""
        mesh = self.load_data()
        lon = np.arange(-180, 180, 1 / 3.0, dtype="float32") + 1 / 3.0
        lat = np.arange(-90, 90, 1 / 3.0, dtype="float32") + 1 / 3.0
        x, y = np.meshgrid(lon, lat, indexing="ij")
        z0, _ = mesh.inverse_distance_weighting(np.vstack(
            (x.flatten(), y.flatten())).T,
                                                within=False,
                                                radius=35434,
                                                k=8,
                                                num_threads=0)
        z1, _ = mesh.inverse_distance_weighting(np.vstack(
            (x.flatten(), y.flatten())).T,
                                                within=False,
                                                radius=35434,
                                                k=8,
                                                num_threads=1)
        z0 = np.ma.fix_invalid(z0)
        z1 = np.ma.fix_invalid(z1)
        self.assertTrue(np.all(z1 == z0))

        if HAVE_PLT:
            plot(x, y, z0.reshape((len(lon), len(lat))), "mss_rtree_idw.png")

    def test_rtree_insert(self):
        """Data insertion test"""
        mesh = self.load_data(packing=False)
        self.assertIsInstance(mesh, core.RTreeFloat32)
        self.assertTrue(len(mesh) != 0)

    def test_rtree_pickle(self):
        """Serialization test"""
        interpolator = self.load_data()
        other = pickle.loads(pickle.dumps(interpolator))
        self.assertTrue(isinstance(other, core.RTreeFloat32))


if __name__ == "__main__":
    unittest.main()
