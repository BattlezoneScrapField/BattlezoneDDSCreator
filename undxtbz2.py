import os, sys
from ctypes import Structure, c_uint32, c_int, c_uint, c_ubyte
from struct import pack, unpack

# If True, only the largest mip map will be used when converting .dxtbz2 to .dds
SINGLE_MIP = False

# If True, automatically overwrites existing output files
OVERWRITE_EXISTING = False

DWORD = c_uint32
DXGI_FORMAT = c_uint32
D3D10_RESOURCE_DIMENSION = c_uint32


class DXTBZ2Header(Structure):
    _fields_ = [
        ("m_Sig", c_int),
        ("m_DXTLevel", c_int),
        ("m_1x1Red", c_ubyte),
        ("m_1x1Green", c_ubyte),
        ("m_1x1Blue", c_ubyte),
        ("m_1x1Alpha", c_ubyte),
        ("m_NumMips", c_int),
        ("m_BaseHeight", c_int),
        ("m_BaseWidth", c_int)
    ]


class DDS_PIXELFORMAT(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwFlags", DWORD),
        ("dwFourCC", DWORD),
        ("dwRGBBitCount", DWORD),
        ("dwRBitMask", DWORD),
        ("dwGBitMask", DWORD),
        ("dwBBitMask", DWORD),
        ("dwABitMask", DWORD)
    ]


class DDS_HEADER(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwFlags", DWORD),
        ("dwHeight", DWORD),
        ("dwWidth", DWORD),
        ("dwPitchOrLinearSize", DWORD),
        ("dwDepth", DWORD),
        ("dwMipMapCount", DWORD),
        ("dwReserved1", DWORD * 11),  # dwReserved1[11]
        ("ddspf", DDS_PIXELFORMAT),
        ("dwCaps", DWORD),
        ("dwCaps2", DWORD),
        ("dwCaps3", DWORD),
        ("dwCaps4", DWORD),
        ("dwReserved2", DWORD)
    ]


class DDS_HEADER_DXT10(Structure):
    _fields_ = [
        ("dxgiFormat", DXGI_FORMAT),
        ("resourceDimension", D3D10_RESOURCE_DIMENSION),
        ("miscFlag", c_uint),
        ("arraySize", c_uint),
        ("miscFlags2", c_uint)
    ]


# DDS_HEADER.dwFlags
DDSD_CAPS = 0x1  # Required in every .dds file.
DDSD_HEIGHT = 0x2  # Required in every .dds file.
DDSD_WIDTH = 0x4  # Required in every .dds file.
DDSD_PITCH = 0x8  # Required when pitch is provided for an uncompressed texture.
DDSD_PIXELFORMAT = 0x1000  # Required in every .dds file.
DDSD_MIPMAPCOUNT = 0x20000  # Required in a mipmapped texture.
DDSD_LINEARSIZE = 0x80000  # Required when pitch is provided for a compressed texture.
DDSD_DEPTH = 0x800000  # Required in a depth texture.

# DDS_PIXELFORMAT.dwFlags
DDPF_ALPHAPIXELS = 0x1  # Texture contains alpha data; dwRGBAlphaBitMask contains valid data.
DDPF_ALPHA = 0x2  # Used in some older DDS files for alpha channel only uncompressed data (dwRGBBitCount contains the alpha channel bitcount; dwABitMask contains valid data)
DDPF_FOURCC = 0x4  # Texture contains compressed RGB data; dwFourCC contains valid data.
DDPF_RGB = 0x40  # Texture contains uncompressed RGB data; dwRGBBitCount and the RGB masks (dwRBitMask, dwGBitMask, dwBBitMask) contain valid data.
DDPF_YUV = 0x200  # Used in some older DDS files for YUV uncompressed data (dwRGBBitCount contains the YUV bit count; dwRBitMask contains the Y mask, dwGBitMask contains the U mask, dwBBitMask contains the V mask)
DDPF_LUMINANCE = 0x20000  # Used in some older DDS files for single channel color uncompressed data (dwRGBBitCount contains the luminance channel bit count; dwRBitMask contains the channel mask). Can be combined with DDPF_ALPHAPIXELS for a two channel DDS file.

# dwCaps
DDSCAPS_COMPLEX = 0x8  # Optional; must be used on any file that contains more than one surface (a mipmap, a cubic environment map, or mipmapped volume texture).
DDSCAPS_TEXTURE = 0x1000  # Required
DDSCAPS_MIPMAP = 0x400000  # Optional; should be used for a mipmap.


def dxtbz2_to_dds(dxtbz2_path, dds_path):
    with open(dxtbz2_path, "rb") as dxtbz2:
        header = DXTBZ2Header()
        dds_header = DDS_HEADER()
        size = DWORD()

        dxtbz2.readinto(header)
        dxtbz2.readinto(size)

        # How to derive proper dxgiFormat from dxtbz2?
        has_alpha = size.value // header.m_BaseHeight == header.m_BaseHeight

        with open(dds_path, "wb") as dds:
            dds_header.dwSize = 124
            dds_header.dwFlags = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT
            dds_header.dwHeight = header.m_BaseHeight
            dds_header.dwWidth = header.m_BaseWidth
            dds_header.dwDepth = 0
            dds_header.dwMipMapCount = 1 if SINGLE_MIP else header.m_NumMips
            dds_header.dwCaps = DDSCAPS_TEXTURE

            dds_header.ddspf.dwSize = 32

            dds_header.ddspf.dwFlags = DDPF_FOURCC
            if has_alpha:
                dds_header.ddspf.dwFlags |= DDPF_ALPHAPIXELS

            dds_header.ddspf.dwFourCC = unpack("I", b"DX10")[0]

            # dds_header.ddspf.dwFourCC = unpack("I", b"\0\0\0\0")[0]
            # dds_header.ddspf.dwRGBBitCount = 32
            # dds_header.ddspf.dwRBitMask = 0x00FF0000 # Red
            # dds_header.ddspf.dwGBitMask = 0x0000FF00 # Blue
            # dds_header.ddspf.dwBBitMask = 0x000000FF # Green
            # dds_header.ddspf.dwABitMask = 0xFF000000 # Alpha

            dds.write(b"DDS ")
            dds.write(dds_header)

            if True:  # FourCC is DX10
                dds_header_ex = DDS_HEADER_DXT10()

                # https://learn.microsoft.com/en-us/windows/win32/api/dxgiformat/ne-dxgiformat-dxgi_format
                # dds_header_ex.dxgiFormat = 87 # DXGI_FORMAT_B8G8R8A8_UNORM = 87
                if has_alpha:
                    dds_header_ex.dxgiFormat = 77  # DXGI_FORMAT_BC3_UNORM = 77 # Works for transparent textures
                else:
                    dds_header_ex.dxgiFormat = 71  # DXGI_FORMAT_BC1_UNORM = 71 # Works for opaque textures

                dds_header_ex.resourceDimension = 3  # DDS_DIMENSION_TEXTURE2D = 3
                # dds_header_ex.miscFlag = 0
                dds_header_ex.arraySize = 1
                # dds_header_ex.miscFlags2 = 0

                dds.write(dds_header_ex)

            for mipmap_index in range(dds_header.dwMipMapCount):
                chunk_data = dxtbz2.read(size.value)
                # print("Writing Chunk %d/%d (%d bytes)" % (mipmap_index+1, dds_header.dwMipMapCount, len(chunk_data)))
                dds.write(chunk_data)

                if not chunk_data or not dxtbz2:
                    print("Unexpected end of data in %r" % dxtbz2_path)
                    break

                dxtbz2.readinto(size)


if __name__ == "__main__":
    file = "./dxtbz2/wire_ivrbomb"
    file_dxtbz2 = file + ".dxtbz2"
    output_file = file + ".dds"
    # User safety - Do not overwrite any existing files.
    if OVERWRITE_EXISTING or not os.path.exists(output_file):
        print(">", file_dxtbz2, "->", output_file)
        dxtbz2_to_dds(file_dxtbz2, output_file)
    else:
        print("File %r already exists." % output_file)
