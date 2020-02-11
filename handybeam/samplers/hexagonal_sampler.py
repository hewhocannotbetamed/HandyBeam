## Imports

import numpy as np
from pyquaternion import Quaternion
from handybeam.misc import copy_docstring
from handybeam.samplers.abstract_sampler import AbstractSampler
import handybeam.visualise
import warnings
warnings.warn('HexagonalSampler is deprecated, use CList sampler instead', DeprecationWarning)
## Global variables

tau = 2*np.pi

## Class

class HexagonalSampler(AbstractSampler):

    '''This is the hexagonal sampling grid class. It takes the specification for a
    hexagonal sampling array and then samples the acoustic field at these points.

    '''

    def __init__(self,
                parent = None,
                normal_vector = np.array((0,0,1)),
                parallel_vector = np.array((0,1,0)),
                origin = np.array((0,0,200e-3)),
                grid_spacing_per_wavelength = 0.2,
                grid_spacing_per_m = None,
                grid_extent_around_origin = 0.2,
                local_work_size = (1,1,1)):

        '''This method intialises an instance of the HexagonalSampler class.

        Parameters
        ----------

        parent : handybeam.world.World
                This is an instance of the handybeam world class. 
        normal_vector : numpy array
                This is the vector normal to the desired sampling grid.
        parallel_vector : numpy array
                This is a vector parallel to the desired sampling grid.
        origin : numpy array
                This is a vector specifying the origin of the sampling grid.
        grid_spacing_per_wavelength : float 
                This specifies the grid spacing as a fraction of the medium wavelength.
        grid_spacing_per_m : float
                This specifies the grid spacing in meters.
        grid_extent_around_origin : float
                This specifies the distance between the origin of the sampling grid and the edge.
        local_work_size : tuple
                This sets the local work size for the GPU, not recommended to change unless the user
                has experience with OpenCL and pyopencl.
        '''
        warnings.warn('HexagonalSampler is deprecated, use CList sampler instead', DeprecationWarning)
        super(HexagonalSampler, self).__init__()

        self.parent = parent
        self.normal_vector = normal_vector
        self.parallel_vector = parallel_vector
        self.vector_2 = None
        self.origin = origin
        self.local_work_size = local_work_size

        if grid_spacing_per_m is None:

            self.delta = grid_spacing_per_wavelength * self.parent.medium_wavelength
            self.side_length = np.int(np.ceil((2*grid_extent_around_origin)/self.delta))
        
        else:
            
            self.delta = grid_spacing_per_m 
            self.side_length = np.int(np.ceil((2*grid_extent_around_origin)/ self.delta))
            
        self.grid_length = np.int32(2*self.side_length - 1) 
        
        self.x_lim = None
        self.y_lim = None
        self.vx1 = None
        self.vy1 = None
        self.vz1 = None
        self.x0 = None
        self.y0 = None
        self.z0 = None
        self.vx2 = None
        self.vy2 = None
        self.vz2 = None

        self.pressure_field = np.zeros((self.grid_length,self.grid_length,1),dtype = np.complex)
        self.coordinates = np.zeros((self.grid_length,self.grid_length,3),dtype = np.float32)

        self.generate_propagation_parameters()
        self.find_hex_grid_area()

    def find_hex_grid_area(self):

        '''This method finds the area of the requested sampling grid.

        '''

        points_in_hex = np.sum([6*k for k in range(1,self.side_length)]) + 1
        points_in_par = np.power(self.grid_length,2)

        area_of_par = np.power((self.grid_length - 1) * self.delta,2) * np.sqrt(3)/2
        self.area = (points_in_hex/points_in_par) * area_of_par


     
    def generate_propagation_parameters(self):

        '''This method finds the parameters to pass to the opencl kernel to correctly
        define the sampling grid. 

        '''

        # Find the unit normal vector to the plane. 

        unit_normal = (1/np.linalg.norm(self.normal_vector))*self.normal_vector
            
        # Define the quaternion required to rotate the parallel vector by an angle of pi/2. 

        quaternion = Quaternion(axis=[unit_normal[0], unit_normal[1],unit_normal[2]], angle = tau/6)

        # Rotate the parallel vector to get a new vector which is perpendicular to the normal and the parallel vector.

        self.vector_2 = quaternion.rotate(self.parallel_vector)
            
        # Find the norm of these vectors.

        parallel_vector_norm = np.linalg.norm(self.parallel_vector) 
        vector_2_norm = np.linalg.norm(self.vector_2)
            
        # Find the unit vectors.

        unit_parallel_vector = (1/parallel_vector_norm)*self.parallel_vector

        unit_vector_2 = (1/vector_2_norm)*self.vector_2

        # Compute the angle between these vectors to check that is equal to pi/2.

        angle_1 = int(np.round(np.rad2deg(np.arccos(np.dot(unit_parallel_vector,unit_vector_2))),1))

        # Compute the angle between each of these vectors and the normal to ensure that they parameterise the plane perpendicular to the nromal. 

        angle_2 = int(np.round(np.rad2deg(np.arccos( np.dot(self.parallel_vector,self.normal_vector) / (parallel_vector_norm*vector_2_norm) )),1))
        angle_3 = int(np.round(np.rad2deg(np.arccos( np.dot(self.vector_2,self.normal_vector) / (parallel_vector_norm*vector_2_norm) )),1))

        # Throw error if they are not.

        if np.bitwise_or(angle_1 != 60,  np.bitwise_or(int(angle_2) != 90, int(angle_3) != 90)):

            raise Exception('Could not parameterise the requested sampling grid correctly!')

        self.vx1 = np.float32(self.parallel_vector[0])
        self.vy1 = np.float32(self.parallel_vector[1])
        self.vz1 = np.float32(self.parallel_vector[2])
        self.x0 = np.float32(self.origin[0])
        self.y0 = np.float32(self.origin[1])
        self.z0 = np.float32(self.origin[2])
        self.vx2 = np.float32(np.round(self.vector_2[0],4))
        self.vy2 = np.float32(np.round(self.vector_2[1],4))
        self.vz2 = np.float32(np.round(self.vector_2[2],4))
        

    def propagate(self,print_performance_feedback = False):

        '''This method calls the hex_propagator to propagate the acoustic field to
        the desired sampling points.

        Parameters
        ----------

        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        kernel_output = self.parent.propagator.hex_propagator(    
                                                            self.parent.tx_array,
                                                            self.side_length,
                                                            self.delta,
                                                            self.x0,self.y0,self.z0,
                                                            self.vx1,self.vy1,self.vz1,
                                                            self.vx2,self.vy2,self.vz2,
                                                            local_work_size = self.local_work_size,
                                                            print_performance_feedback = print_performance_feedback
                                                        )
                                                        

        self.pressure_field= kernel_output[:,:,3] + np.complex(0,1) * kernel_output[:,:,4]
        self.coordinates = kernel_output[:,:,0:4]
 