"""
.. the following is a link to enable linking to this file:
.. solver_:

Contains excitation solvers.

A basic single-point-focus excitation solver is :meth:`handybeam.solver.Solver.single_focus_solver`

"""
# Imports
import warnings
warnings.warn('solver.py is obsolete - use beamformer.py instead')

import handybeam.opencl_wrappers.solver_wrappers as solver_wrappers

# Class


class Solver:
    """" Contains the OpenCL subsystem for single focus solver.
    
    This class calls the OpenCL wrapper for the single focus solver. 

    """

    def __init__(self, parent=None):
        """ Initializes an instance of class Solver.

        Parameters
        ----------

        parent : handybeam.world.World()
                This is an instance of the handybeam world class.
        
        """
        
        self.parent = parent
        self.solver = solver_wrappers.Solver(parent=self.parent)
    
    def single_focus_solver(self, x_focus, y_focus, z_focus, local_work_size=(1, 1, 1), print_performance_feedback=False):
        """ Solve excitation coefficients for a single focal point
        
        This method calls the OpenCL wrapper mixin class single_focus_solver which determines
        the set of activation coefficients required to produce a single focal point a given point in space. 

        Parameters
        ----------

        x_focus : numpy float
                This is the x-coordinate of the requested focal point position.
        y_focus : numpy float
                This is the y-coordinate of the requested focal point position.
        z_focus : numpy float
                This is the z-coordinate of the requested focal point position.          
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance statistics.
        
        """

        kernel_output = self.solver.single_focus_solver(    
                                                            self.parent.tx_array,
                                                            x_focus, y_focus, z_focus,
                                                            local_work_size=local_work_size,
                                                            print_performance_feedback=print_performance_feedback
                                                        )

        self.parent.tx_array.tx_array_element_descriptor = kernel_output
     
    def set_parent(self, new_parent):
        """ changes the parent of an instance of the class Solver.

        Parameters
        ----------

        new_parent : handybeam.world.World()
                This is an instance of the handybeam world class.

        """
        
        self.parent = new_parent


