"""
.. _tx_array:

.. ===============================
   Module :code:handybeam.tx_array
   ===============================

contains the TxArray class

example usage:

.. code-block:: python

    world.tx_array = handybeam.tx_array_library.rectilinear(parent = world)


"""

## Imports

import numpy as np
import handybeam.visualise
from handybeam.remember_instance_creation_info import RememberInstanceCreationInfo
from os import linesep

## Global variables

## Class


class TxArray(RememberInstanceCreationInfo):
    """ Describes the transmitter array

    Primarily holds the :code:`tx_array_element_descriptor`

    Attributes:
        tx_array_element_descriptor: (numpy.array) compact buffer describing the array. See :ref:`b_tx_array_compact_descriptor:tx_element_array_descriptor_a`
        name: (string). user-readable string/elements


    """

    def set_name(self, value):
        self._name = value

    def get_name(self):
        return self._name

    name = property(get_name, set_name)

    def __init__(self, parent=None):
        """ Constructor

        :param parent: handybeam.world.World
            set to current world instance.

        """

        super().__init__()
        self.parent = parent
        self.tx_array_element_descriptor = self.generate_tx_array_element()
        self._name = "default single-element array"

    def generate_empty_tx_element_descriptor(self):
        
        '''DESCRIPTION HERE

        '''
        q = np.zeros((1, 16), dtype=np.float)
        q[0, 5] = np.float(1.0)  # make sure that this element has a non-broken normal vector
        return q

    def generate_tx_array_element(self,
                                  x: float = 0.0, y: float = 0.0, z: float = 0.0,
                                  xnormal: float = 0.0, ynormal: float = 0.0, znormal: float = 1.0,
                                  directivity_phase_poly1_c1: float = 0.0,
                                  directivity_amplitude_poly2_c0: float = 318.5,
                                  directivity_amplitude_poly2_c1: float = -682.4,
                                  directivity_amplitude_poly2_c2: float = 461.33,
                                  amplitude_ratio_setting: float = 1.0,
                                  phase_setting: float = 0.0
                         ):
        ''' builds a single line of :ref:`b_tx_array_compact_descriptor:tx_element_array_descriptor_a` buffer out of provided named parameters.

        Please note that the directivity defaults are set to match the murata transducer.

        In order to generate an ominidirectional transducer with a reference amplitude of "1" - set
        `directivity_phase_poly1_c1` to 0.0, `directivity_amplitude_poly2_c0` to 1.0, `directivity_amplitude_poly2_c1` to 0.0, and `directivity_amplitude_poly2_c2` to 0.0
        
        Parameters
        ----------

        x : float
                DESCRIPTION HERE
        y : float
                DESCRIPTION HERE
        z : float
                DESCRIPTION HERE
        xnormal : float
                DESCRIPTION HERE
        ynormal : float
                DESCRIPTION HERE
        znormal : float
                DESCRIPTION HERE
        directivity_phase_poly1_c1 : float
                DESCRIPTION HERE
        directivity_amplitude_poly2_c0: float
                DESCRIPTION HERE
        directivity_amplitude_poly2_c1: float
                DESCRIPTION HERE
        directivity_amplitude_poly2_c2 : float
                DESCRIPTION HERE
        amplitude_ratio_setting : float
                DESCRIPTION HERE
        phase_setting : float 
                DESCRIPTION HERE

        '''
        tx_single_element_descriptor = np.zeros((1, 16), dtype=np.float32)
        tx_single_element_descriptor.fill(np.float32(np.NaN))
        tx_single_element_descriptor[0, 0] = np.float32(x)
        tx_single_element_descriptor[0, 1] = np.float32(y)
        tx_single_element_descriptor[0, 2] = np.float32(z)
        tx_single_element_descriptor[0, 3] = np.float32(xnormal)
        tx_single_element_descriptor[0, 4] = np.float32(ynormal)
        tx_single_element_descriptor[0, 5] = np.float32(znormal)
        tx_single_element_descriptor[0, 6] = np.float32(directivity_phase_poly1_c1)
        tx_single_element_descriptor[0, 7] = np.float32(directivity_amplitude_poly2_c0)
        tx_single_element_descriptor[0, 8] = np.float32(directivity_amplitude_poly2_c1)
        tx_single_element_descriptor[0, 9] = np.float32(directivity_amplitude_poly2_c2)
        tx_single_element_descriptor[0, 10] = np.float32(amplitude_ratio_setting)
        tx_single_element_descriptor[0, 11] = np.float32(phase_setting)
        tx_single_element_descriptor[0, 12] = np.float32(np.NaN)
        tx_single_element_descriptor[0, 13] = np.float32(np.NaN)
        tx_single_element_descriptor[0, 14] = np.float32(np.NaN)
        tx_single_element_descriptor[0, 15] = np.float32(np.NaN)

        return tx_single_element_descriptor

    def visualise(self, figsize=(4, 3), dpi=150):
        """ Run the visualizer.

        Run the :meth:`handybeam.visualise.visualise_flat_tx_array()`.

        Note: runs the visualizer on the array that is attached to the parent of this array. So might be misleading sometimes.

        """

        handybeam.visualise.tx_array_basic(self, figsize=figsize, dpi=dpi)

    ## Read-only attributes 

    @property
    def element_count(self):
        """ return count of transmiter elements in this array.

        does :code:`return self.tx_array_element_descriptor.shape[0]`

        """
        return self.tx_array_element_descriptor.shape[0]

    def __str__(self):
        """ information about this array.

        :return: basic information about this array
        """
        return self.name

    def __repr__(self):
        """ links to self.__str__()

        :return: basic information about this array
        """
        return self.creation_text + linesep + "name string: " + self.__str__() + linesep + "count of elements: {}".format(self.tx_array_element_descriptor.shape[0])

    def describe_element(self, idx):
        ed = self.tx_array_element_descriptor[idx, :]
        txt = "element {}: ".format(idx)+linesep
        txt = txt + " >   (location) =({:0.1f}, {:0.1f}, {:0.1f})mm".format(ed[0]*1e3, ed[1]*1e3, ed[2]*1e3)+linesep
        txt = txt + " >    (normals) =({}, {}, {})".format(ed[3], ed[4], ed[5])+linesep
        txt = txt + " > (dir coeffs) =(phase_c1:{}, | amp:({}, {}, {}))".format(ed[6], ed[7], ed[8], ed[9])+linesep
        txt = txt + " >  amp setting ={}".format(ed[10]) + linesep
        txt = txt + " >        phase ={}".format(ed[11]) + linesep
        txt = txt + " >       (nans) =({}, {}, {}, {}) ".format(ed[12], ed[13], ed[14], ed[15])+linesep
        return txt

    def apply_basic_trap_signature_x_split(self):
        """ for all elements with x>0, inverses the phase"""

        for idx in range(self.element_count):
            # if x-coordinate is >0
            if self.tx_array_element_descriptor[idx, 0]>0.0:
                # add pi to phase
                self.tx_array_element_descriptor[idx, 11]=self.tx_array_element_descriptor[idx, 11]+np.pi

    def apply_basic_trap_signature_y_split(self):
        for idx in range(self.element_count):
            # if y-coordinate is >0
            if self.tx_array_element_descriptor[idx, 1] > 0.0:
                # add pi to phase
                self.tx_array_element_descriptor[idx, 11] = self.tx_array_element_descriptor[idx, 11] + np.pi

    def set_directivity_coefficients(self, c0=318.5, c1=-628.4, c2=461.33):
        self.tx_array_element_descriptor[:, 7] = c0
        self.tx_array_element_descriptor[:, 8] = c1
        self.tx_array_element_descriptor[:, 9] = c2


