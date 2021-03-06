'''OpenGL extension SGIX.reference_plane

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_SGIX_reference_plane'
_DEPRECATED = False
GL_REFERENCE_PLANE_SGIX = constant.Constant( 'GL_REFERENCE_PLANE_SGIX', 0x817D )
GL_REFERENCE_PLANE_EQUATION_SGIX = constant.Constant( 'GL_REFERENCE_PLANE_EQUATION_SGIX', 0x817E )
glReferencePlaneSGIX = platform.createExtensionFunction( 
'glReferencePlaneSGIX',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(arrays.GLdoubleArray,),
doc='glReferencePlaneSGIX(GLdoubleArray(equation)) -> None',
argNames=('equation',),
deprecated=_DEPRECATED,
)


def glInitReferencePlaneSGIX():
    '''Return boolean indicating whether this extension is available'''
    return extensions.hasGLExtension( EXTENSION_NAME )
