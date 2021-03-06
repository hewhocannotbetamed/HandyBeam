## Imports 

from handybeam.misc import copy_docstring
import handybeam.visualise
from handybeam.remember_instance_creation_info import RememberInstanceCreationInfo
## Class


class AbstractSampler(RememberInstanceCreationInfo):
    """ Defines the common attributes of each sampler class.
    """

    def __init__(self, parent = None):
        """ Initialises an instance of the AbstractSampler class.

        Parameters
        ----------

        parent : handybeam.world.World
                This is an instance of the handybeam world class. 

        """
        super(AbstractSampler, self).__init__()

        self.parent = None
        self.pressure_field = None
        self.coordinates = None
        self.area = None
        self.volume = None
  
    def set_parent(self, parent):
        """Sets the parent of this instance if one has not been provided.

        Parameters
        ----------

        parent : handybeam.world.World
                This is an instance of the handybeam world class. 

        """

        self.parent = parent

    @copy_docstring(handybeam.visualise.visualise_all_in_one, prepend=True)
    def visualise_all_in_one(self, filename=None):

        return handybeam.visualise.visualise_all_in_one(world=self.parent, sampler=self, filename=filename)

    @copy_docstring(handybeam.visualise.visualise_sampling_grid_and_array, prepend=True)
    def visualise_sampling_grid_and_array(self,
                                          world=None,
                                          sampler=None,
                                          filename=None,
                                          figsize=[15, 10],
                                          dpi=150):
        if world is None:
            world = self.parent
        if sampler is None:
            sampler = self
        return handybeam.visualise.visualise_sampling_grid_and_array(world=world,
                                                                     sampler=sampler,
                                                                     filename=filename,
                                                                     figsize=figsize,
                                                                     dpi=dpi)

    @copy_docstring(handybeam.visualise.visualise_sampling_grid, prepend=True)
    def visualise_sampling_grid(self, filename=None):

        return handybeam.visualise.visualise_sampling_grid(sampler=self, filename=filename)

    @copy_docstring(handybeam.visualise.visualise_3D, prepend=True)
    def visualise_3D(self, threshold=50, colour_map='cubehelix'):

        return handybeam.visualise.visualise_3D(world=self.parent, sampler=self,
                                                threshold=threshold,
                                                colour_map=colour_map)
