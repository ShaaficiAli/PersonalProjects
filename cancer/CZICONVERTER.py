from czifile import*
from tifffile import*
from lxml import*
with CziFile('2.czi') as czi:
    image = czi.asarray()
    xl = czi.metadata

