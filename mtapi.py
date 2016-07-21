#! /usr/bin/env python3

# mtapi.py
#
# Basic classes for MTAPI command construction and parsing


import sys

class ParseError(Exception):
    pass


class MTAPIType:
    STRING = [ "POLL", "SREQ", "AREQ", "SRSP" ]
    def __init__(self, value):
        self.type = (value >> 5) & 0x07

    def __str__(self):
        if self.type < len(MTAPIType.STRING):
            return MTAPIType.STRING[self.type]
        return "RSVD(%02x)" % (self.type << 5)

    @classmethod
    def to_number(cls, name):
        number = cls.STRING.index(name)
        return number << 5


class MTAPISubsystem:
    STRING = [ "Reserved(0x00)",
               "SYS",
               "MAC",
               "NWK",
               "AF",
               "ZDO",
               "SAPI",
               "UTIL",
               "DEBUG",
               "APP" ]
    def __init__(self, value):
        self.subsystem = value & 0x1f

    def __str__(self):
        if self.subsystem < len(MTAPISubsystem.STRING):
            return MTAPISubsystem.STRING[self.subsystem]
        return "Reserved(%02x)" % self.subsystem

    @classmethod
    def to_number(cls, name):
        return cls.STRING.index(name)


class MTAPICmd:
    """Class encapsulating the description of MTAPI commands.  Class
    instances encapsulate individual commands, and the command is parsed
    by calling the instance, supplying the data stream for the command
    body."""
    def __init__(self, name, fields):
        """Create a command parse description called `name`, passing it
        a sequence of field parse description describing the command's
        data."""
        self.name = name
        self.fields = fields

    def __str__(self):
        "Return the name of the command."
        return self.name

    def __call__(self, data):
        """Parse the data into the fields of the command, returning
        the offset into the data at which parsing stops."""
        return parse_generic(self.fields, data)

    def parse_tokens(self, tokens, buf):
        """Parse the textual token stream into binary, and insert it
        into the byte buffer passed in.  Returns True if the token
        stream was parsed successfully, False on a parse error."""
        if len(self.fields) != len(tokens) - 1:
            return False
        for field, token in zip(self.fields, tokens[1:]):
            if not field.parse_token(token, buf):
                return False
        return True


def print_field(indent, field, value):
    "Display a (name, value) pair with appropriate indentation."
    print(" " * (2*indent+1), field, ":", value)


class ParseField:
    "Basic parse description class for data fields of any length."
    def __init__(self, name, length, parser=None):
        """Create a basic parse description for a field called `name`
        that is `length` bytes long.  The data will be displayed as a
        sequence of space-separated byte values prefixed with '0x' by
        default.  If the `parser` argument is not None, it is called
        instead to display the bytes in the field.
        """
        self.name = name
        self.length = length
        self.parser = parser

    def __repr__(self):
        return "ParseField(\"%s\", %d, %s)" % (self.name,
                                           self.length,
                                           self.parser)

    def field_info(self):
        return [(self.name, self.length, self.parser)]

    def parse(self, data, offset, indent=0):
        """Extracts data for the field from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.

        If there is insufficient space in `data` for all the bytes of
        the field, an mtapi.ParseError will be raised.
        """
        if len(data) < offset + self.length:
            raise ParseError("Field %s missing" % self.name)
        byte_range = data[offset : (offset + self.length)]
        if self.parser is not None:
            print_field(indent, self.name, self.parser(byte_range))
        else:
            print_field(indent, self.name,
                        " ".join("0x%02x" % b for b in byte_range))
        return offset + self.length

    def parse_token(self, token, buf):
        """Parses the tokenised input stream of text into binary, and
        stores it in the MTBuffer provided.  Returns True on success,
        False on failure."""
        try:
            value = int(token, 0)
        except ValueError:
            return False
        for i in range(self.length):
            buf.append((value >> (8*i)) & 0xff)
        return True


class ParseClusterList:
    """Slightly misnamed description class for a list of two-byte
    data items prefixed with a single byte containing the number of
    items.  Generally but not exclusively used for list of cluster Ids.
    The two-byte numbers are parsed little-endian, and written out with
    no prefix (i.e. no leading '0x').
    """
    def __init__(self, count_name, list_name):
        """Create a parse description for a list of two-byte values
        called `list_name` with a leading count field called `count_name`.
        """
        self.name = count_name
        self.list_name = list_name

    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.  The two-byte values are
        listed in hexadecimal with no leading '0x', separated by a comma
        and a space.

        If there is insufficient space in `data` for all the bytes of
        the fields, an mtapi.ParseError will be raised.
        """
        if len(data) <= offset:
            raise ParseError("Field %s missing" % self.name)
        count = data[offset]
        print(" " * (2*indent+1), self.name, ":", count)
        clusters = []
        offset += 1
        if len(data) < offset + 2*count:
            raise ParseError("Field %s missing or short" % self.list_name)
        while count > 0:
            cluster = data[offset] | (data[offset+1] << 8)
            clusters.append(cluster)
            offset += 2
            count -= 1
        print_field(indent, self.list_name,
                    ", ".join("%04x" % cluster for cluster in clusters))
        return offset


class ParseVariable:
    """Parse description class for a variable length byte stream
    prefixed with a length field, optionally of limited length."""
    def __init__(self, length_name, data_name, len_bytes=1, limit=None):
        """Create a parse description for a list of byte values called
        `data_name` with a leading count field of `len_bytes` bytes
        called `length_name`.  If the `limit` parameter is given, the
        count field may not specify a length of more than `limit` bytes.
        """
        self.name = length_name
        self.data_name = data_name
        self.len_bytes = len_bytes
        self.limit = limit

    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.  The byte values are
        listed in hexadecimal with no leading '0x', separated by a
        space.

        If there is insufficient space in `data` for all the bytes of
        the fields, an mtapi.ParseError will be raised.
        """
        if len(data) < offset + self.len_bytes:
            raise ParseError("Field %s missing or short" % self.name)
        len_bytes = self.len_bytes
        count = 0
        while len_bytes > 0:
            count = (count << 8) | data[offset + len_bytes - 1]
            len_bytes -= 1
        if self.limit is not None and count > self.limit:
            raise ParseError("Variable field %s exceeds limit (%d > %d)" %
                             (self.name, count, self.limit))
        print_field(indent, self.name, count)
        if len(data) < offset + self.len_bytes + count:
            raise ParseError("Field %s missing or short" % self.data_name)
        print_field(indent, self.data_name,
                    " ".join("%02x" % d
                             for d in data[offset+self.len_bytes:
                                           offset+count+self.len_bytes]))
        return offset + count + self.len_bytes


class ParseExtData:
    """Parse description class for a variable length byte stream
    prefixed with a two-byte length field, that has a length limit.
    If the announced length is greater than the limit, the data is
    omitted, being transferred in segments in different packets."""
    def __init__(self, length_name, data_name, limit):
        """Create a parse description for a list of byte values called
        `data_name` with a leading two-byte count field called
        `length name` and a maximum number of bytes present of `limit`.
        """
        self.name = length_name
        self.data_name = data_name
        self.limit = limit

    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.  The byte values are
        listed in hexadecimal with no leading '0x', separated by a
        space.  If there is no data because the count field exceeds
        the limit, the string "Blank" will be displayed as the data.

        If there is insufficience space in `data` for all the bytes of
        the fields, an mtapi.ParseError will be raised.
        """
        if len(data) <= offset + 1:
            raise ParseError("Field %s is missing or short" % self.name)
        count = (data[offset+1] << 8) | data[offset]
        print_field(indent, self.name, count)
        if count > self.limit:
            print_field(indent, self.data_name, "Blank")
            return offset + 2
        if len(data) < offset + 2 + count:
            raise ParseError("Field %s is missing or short" %
                             self.data_name)
        print_field(indent, self.data_name,
                    " ".join("%02x" % d
                             for d in data[offset+2: offset+count+2]))
        return offset + count + 2


class ParseRemaining:
    """Parse description class for a field consisting of all the
    remaining bytes in a stream."""
    def __init__(self, name):
        "Create a parse description for a list of bytes called `name`"
        self.name = name

    def parse(self, data, offset, indent=0):
        """Extracts all the data from `offset` bytes into the `data`
        bytestream, and  prints the parsed results.  The output has
        2 * `indent` + 2 leading spaces.  The byte values are listed
        in hexadecimal with no leading '0x', separated by a space."""
        print_field(indent, self.name,
                    " ".join("%02x" % d for d in data[offset:]))
        return len(data)


class ParseAddress:
    """Parse description class for a pair of fields consisting of an
    address mode followed by the address it describes.  The address
    itself will always take up 8 bytes even if it is smaller or omitted
    entirely.  Unused bytes are ignored and may contain anything."""
    def __init__(self, mode_name, addr_name):
        """Create a parse description for an address mode field called
        `mode_name` and its associated address `addr_name`."""
        self.name = mode_name
        self.addr_name = addr_name

    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.  Two-byte address fields
        are printed as a four digit hexadecimal value with no leading
        '0x'; eight-byte (IEEE) address fields are read in little
        endian and printed as a big endian colon-separated list of
        hexadecimal byte values, in the usual format for MAC addresses."""
        if len(data) < offset:
            raise ParseError("Field %s is missing" % self.name)
        if len(data) < offset + 9:
            raise ParseError("Field %s is missing or short" %
                             self.addr_name)
        mode = data[offset]
        if mode == 3:
            print_field(indent, self.name, "64-bit")
            print_field(indent, self.addr_name,
                        ":".join("%02x" % b
                                 for b in data[offset+8:offset:-1]))
        elif mode == 2:
            print_field(indent, self.name, "16-bit")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
        elif mode == 1:
            print_field(indent, self.name, "Group address")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
        elif mode == 0:
            print_field(indent, self.name, "Address not present")
        elif mode == 0xff:
            print_field(indent, self.name, "Broadcast")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
        else:
            print_field(indent, self.name, "Unknown(%02x)" % mode)
            print_field(indent, self.addr_name,
                        " ".join("0x%02x" % b
                                 for b in data[offset+1:offset+9]))
        return offset + 9


class ParseBindAddress:
    """Parse Description for a bind address combination, being an
    address mode, a two- or eight-byte address (if present) and an
    endpoint (if an eight-bytes address was used).  Unlike ParseAddress,
    only those bytes actually required are read from the stream and no
    padding is employed."""
    def __init__(self, mode_name, addr_name, ep_name):
        """Creates a parse description for an address mode field called
        `mode_name` with an associated optional address `addr_name` and
        optional endpoint `ep_name`."""
        self.name = mode_name
        self.addr_name = addr_name
        self.ep_name = ep_name

    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  The output
        has 2 * `indent` + 2 leading spaces.  Two-byte address fields
        are printed as a four digit hexadecimal value with no leading
        '0x'; eight-byte (IEEE) address fields are read in little
        endian and printed as a big endian colon-separated list of
        hexadecimal byte values, in the usual format for MAC addresses.
        The endpoint is printed as a two digit hexadecimal value with
        no leading '0x'."""
        if len(data) <= offset:
            raise ParseError("Field %s is missing" % self.name)
        mode = data[offset]
        if mode == 0:
            print_field(indent, self.name, "Address not present")
            return offset + 1
        if mode == 1:
            if len(data) < offset + 3:
                raise ParseError("Field %s is missing or short" %
                                 self.addr_name)
            print_field(indent, self.name, "Group address")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
            return offset + 3
        if mode == 2:
            if len(data) < offset + 3:
                raise ParseError("Field %s is missing or short" %
                                 self.addr_name)
            print_field(indent, self.name, "16-bit")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
            return offset + 3
        if mode == 3:
            if len(data) < offset + 9:
                raise ParseError("Field %s is missing or short" %
                                 self.addr_name)
            if len(data) == offset + 9:
                raise ParseError("Field %s is missing" % self.ep_name)
            print_field(indent, self.name, "64-bit")
            print_field(indent, self.addr_name,
                        ":".join("%02x" % b
                                 for b in data[offset+8:offset:-1]))
            print_field(indent, self.ep_name, "%02x" % data[offset+9])
            return offset + 10
        if mode == 0xff:
            if len(data) < offset + 3:
                raise ParseError("Field %s is missing or short" %
                                 self.addr_name)
            print_field(indent, self.name, "Broadcast")
            print_field(indent, self.addr_name,
                        "%04x" % (data[offset+1] |
                                  (data[offset+2] << 8)))
            return offset + 3
        raise ParseError("Invalid field %s (%02x)" % (self.name,
                                                      data[offset]))


class ParseInterPan:
    """Parse description for an Inter-Pan command plus parameters."""
    def parse(self, data, offset, indent=0):
        """Extracts the command field from `offset` bytes into the
        `data` bytestream, and depending on that byte may read more
        bytes as command parameters.  It prints the parsed results
        with 2 * `indent` + 2 leading spaces."""
        if len(data) <= offset:
            raise ParseError("Field Command is missing")
        command = data[offset]
        if command == 0:
            print_field(indent, "Command", "InterPanClr")
            return offset + 1
        if command == 1:
            if len(data) == offset + 1:
                raise ParseError("Field Channel is missing")
            print_field(indent, "Command", "InterPanSet")
            print_field(indent, "Channel", data[offset+1])
            return offset + 2
        if command == 2:
            if len(data) == offset + 1:
                   raise ParseError("Field Endpoint is missing")
            print_field(indent, "Command", "InterPanReg")
            print_field(indent, "Endpoint", "0x%02x" % data[offset+1])
            return offset + 2
        if command != 3:
            raise ParseError("Unknown InterPan command 0x%02x" % command)
        if len(data) <= offset + 2:
            raise ParseError("Field PanId is missing or short")
        if len(data) == offset + 3:
            raise ParseError("Field Endpoint is missing")
        print_field(indent, "Command", "InterPanChk")
        print_field(indent, "PanId",
                    "%04x" % (data[offset+1] |
                              (data[offset+2] << 8)))
        print_field(indent, "Endpoint", "0x%02x" % data[offset+3])
        return offset + 4


class BitField:
    """Helper class to describe a bitfield within an arbitrary length
    integer, and parse just that field out."""
    def __init__(self, field):
        """Create the parse description for a single bitfield.  The
        `field` parameter is a two-element sequence (for convenience
        of the primary parsing class); the first element is the name
        of the bitfield, and the second is a mask that is applied to
        extract the field from data."""
        self.name = field[0]
        self.mask = field[1]
        self.shift = 0
        if self.mask == 0:
            raise ParseError("Empty mask illegal in bitfield '%s'" %
                             self.name)
        mask = self.mask
        while (mask & 1) == 0:
            mask >>= 1
            self.shift += 1

    def parse(self, byte, indent=0):
        """Extracts the bitfield from the integer `byte` presented,
        and prints the results right-shifted so that the least
        significant bit of the field is bit 0.  The output has
        2 * `indent` + 2 leading spaces, and is two hexadecimal
        digits long with no leading '0x'."""
        print_field(indent, self.name,
                    "%02x" % ((byte & self.mask) >> self.shift))


class ParseBitFields:
    """Parse description class for single bytes that contain multiple
    bitfields.  Individual bitfields within the byte are handled by the
    BitField class."""
    def __init__(self, fields):
        """Create the parse description for a byte full of bitfields.
        The `fields` parameter is a sequence of two-item sequences,
        each two-item sequence being the `(name, mask)` pair required
        to initialise a BitField.  The overall name of the byte is a
        combination of the names of the individual fields separated by
        slashes."""
        self.name = "/".join(f[0] for f in fields)
        self.fields = [BitField(f) for f in fields]

    def parse(self, data, offset, indent=0):
        """Extracts the byte to examine from `offset` bytes into the
        `data` bytestream, and calls the individual BitField parsers
        to output the data.  The overall field name is printed with
        2 * `indent` + 2 leading spaces, while the bitfields themselves
        have an extra two leading spaces."""
        if len(data) <= offset:
            raise ParseError("Field %s is missing" % self.name)
        byte = data[offset]
        print_field(indent, self.name, "")
        for f in self.fields:
            f.parse(byte, indent+1)
        return offset + 1


class ParseRepeated:
    """Description class for a field that consists of a number of
    repetitions of a sequence of subfields.  On parsing, the subfields
    are printed with a greater indentation than the original."""
    def __init__(self, count_name, field_name, fields):
        """Create a parse description for a single-byte count field
        called `count` giving the number of repetitions of a sequence
        of `fields` collectively called `field_name`."""
        self.count_name = count_name
        self.field_name = field_name
        self.fields = fields

    def parse(self, data, offset, indent=0):
        """Extracts the repetition count from `offset` bytes into the
        `data` bytestream, then calls parse_generic() to parse each
        field in the `fields` sequence, calling as many times as
        indicated by the count."""
        if len(data) <= offset:
            raise ParseError("Field %s is missing" % self.count_name)
        count = data[offset]
        print_field(indent, self.count_name, count)
        print_field(indent, self.field_name, "")
        offset +=1
        while count > 0:
            import sys
            field_len = parse_generic(self.fields, data[offset:], indent+1)
            offset += field_len
            count -= 1
        return offset

class ParseKey:
    """Parse description class for a security key.  The class combines
    an 8 byte security source, a single byte security level, a single
    byte of key ID mode, and a single byte of the key index itself."""
    SECURITY_LEVEL = { 0x00: "No Security",
                       0x01: "MIC_32_AUTH",
                       0x02: "MIC_64_AUTH",
                       0x03: "MIC_128_AUTH",
                       0x04: "AES_ENCRYPTION",
                       0x05: "AES_ENCRYPTION_MIC_32",
                       0x06: "AES_ENCRYPTION_MIC_64",
                       0x07: "AES_ENCRYPTION_MIC_128"
    }

    KEY_ID_MODE = { 0x00: "Not Used",
                    0x01: "KEY_1BYTE_INDEX",
                    0x02: "KEY_4BYTE_INDEX",
                    0x03: "KEY_8BYTE_INDEX"
    }

    def __init__(self, source, security, id_mode, index):
        """Create a parse class description for a security key, with
        a source field called `source`, a security level field called
        `security`, a security ID mode called `id_mode`, and a key
        index called `index`."""
        self.source_name = source
        self.security_name = security
        self.id_mode_name = id_mode
        self.index_name = index

    def parse(self, data, offset, indent=0):
        """Extracts data from `offset` bytes into the `data` bytestream
        and prints the parsed results.  Each field has 2 * `indent` + 2
        leading spaces.  The source field is presented as eight two-digit
        space-separated hexadecimal values with no leading '0x', in the
        order encountered in the bytestream.  The security level and ID
        mode are rendered as text, and the key index is a single two
        digit hexadecimal value with no leading '0x'."""
        if len(data) <= offset + 8:
            raise ParseError("Field %s is missing or short" %
                             self.source_name)
        if len(data) == offset + 8:
            raise ParseError("Field %s is missing" % self.security_name)
        if len(data) == offset + 9:
            raise ParseError("Field %s is missing" % self.id_mode_name)
        if len(data) == offset + 10:
            raise ParseError("Field %s is missing" % self.index_name)
        print_field(indent, self.source_name,
                    " ".join("%02x" % s for s in data[offset:offset+8]))
        print_field(indent, self.security_name,
                    ParseKey.SECURITY_LEVEL.get(
                        data[offset+8],
                        "Invalid(%02x)" % data[offset+8]))
        print_field(indent, self.id_mode_name,
                    ParseKey.KEY_ID_MODE.get(
                        data[offset+9],
                        "Invalid(%02x)"  % data[offset+9]))
        print_field(indent, self.index_name, "%02x" % data[offset+10])
        return offset + 11


class ParseTime:
    """Parse description class for the common fields used for time.
    Uses fixed names for the fields (since life is too short), so takes
    no parameters to its initialiser."""
    def parse(self, data, offset, indent=0):
        """Extracts data for the fields from `offset` bytes into the
        `data` bytestream, and prints the parsed results.  Each field
        is preceded by 2 * `indent` + 2 spaces.  The `UTCTime` field
        takes up four bytes little-endian, and is presented as a decimal
        number with no leading zeroes.  The `Year` field takes up two
        bytes little-endian, and is also presented as an unpadded decimal
        number.  The remaining fields are single bytes, and are presented
        in decimal."""
        if len(data) < offset+4:
            raise ParseError("Field UTCTime is missing or short")
        if len(data) == offset+4:
            raise ParseError("Field Hour is missing")
        if len(data) == offset+5:
            raise ParseError("Field Minute is missing")
        if len(data) == offset+6:
            raise ParseError("Field Second is missing")
        if len(data) == offset+7:
            raise ParseError("Field Month is missing")
        if len(data) == offset+8:
            raise ParseError("Field Day is missing")
        if len(data) <= offset + 10:
            raise ParseError("Field Year is missing or short")
        print_field(indent, "UTCTime",
                    field_parse_word(data[offset:offset+4],
                                     as_decimal=True))
        print_field(indent, "Hour", data[offset+4])
        print_field(indent, "Minute", data[offset+5])
        print_field(indent, "Second", data[offset+6])
        print_field(indent, "Month", data[offset+7])
        print_field(indent, "Day", data[offset+8])
        print_field(indent, "Year",
                    field_parse_hword(data[offset+9:offset+11],
                                      as_decimal=True))
        return offset + 11


def parse_generic(fields, data, indent=0):
    "Recurse through the sequence `fields`, parsing the data into them."
    offset = 0
    for field in fields:
        offset = field.parse(data, offset, indent)
    return offset


# Helper routines for parsing field types into strings

def field_parse_hword(data, as_decimal=False):
    """Parse two bytes as a little-endian integer.  Presents as four
    hexadecimal digits with no leading '0x' unless `as_decimal` is True.
    `data` is assumed to contain at least two bytes."""
    value = data[0] | (data[1] << 8)
    if as_decimal:
        return str(value)
    return "%04x" % value

def field_parse_word(data, as_decimal=False):
    """Parse four bytes as a little-endian integer.  Presents as eight
    hexadecimal digits with no leading '0x' unless `as_decimal` is True.
    `data` is assumed to contain at least four bytes."""
    value = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)
    if as_decimal:
        return str(value)
    return "%08x" % value

def field_parse_colon_sep(data):
    """Reverse the order of the bytes presented and return them as
    two digit hexadecimal numbers with no leading '0x', separated by
    colons.  This is largely intended for IEEE MAC addresses."""
    return ":".join("%02x" % d for d in data[-1::-1])

def field_parse_scan_channels(data):
    """Interpret a four byte little-endian integer as a bitfield of
    channel numbers, and print the result as a comma-separated list of
    decimal channel numbers.  If no channels are present, the string
    "None" is return; if all the legal channels are present, the string
    "All" is return.  Otherwise no attempt is made to ensure that the
    channels listed are legal in any domain, and `data` is assumed to
    contain at least four bytes."""
    value = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)
    if value == 0:
        return "None"
    if value == 0x07fff800:
        return "All"
    channels = []
    for i in range(32):
        if value & (1 << i):
            channels.append(i)
    return ",".join(str(channel) for channel in channels)

def field_parse_dict(data, dictionary, default):
    """Interpret the `data` bytes passed in as a little endian integer,
    look the value up in `dictionary`, return the value if found or
    `default` if not.  `default` may contain a '%' formatting term, and
    will have the interpreted data value as a parameter"""
    value = 0
    for index, d in enumerate(data):
        value |= d << (index * 8)
    if value in dictionary:
        return dictionary[value]
    return default % value


class FieldParseDict:
    def __init__(self, dictionary, default, width=1):
        self.dictionary = dictionary
        self.default = default
        self.width = width

    def __call__(self, data):
        # Assemble the index value
        width = self.width
        value = 0
        while width > 0:
            value = (value << 8) | data[width-1]
            width -= 1
        if value in self.dictionary:
            return self.dictionary[value]
        return self.default % value

    def helper(self, field_name):
        print("Value '%s' codes are:" % field_name)
        fmt = "\t0x%%0%dx: %%s" % (self.width * 2)
        for key in sorted(self.dictionary.keys()):
            print(fmt % (key, self.dictionary[key]))


def field_parse_bitfield(data, bitarray, off_bitarray=None):
    """Interpret the `data` bytes pass in as a little endian integer.
    If bit `n` of the integer is set, display the nth item of the sequence
    of strings `bitarray`; otherwise if `off_bitarray` is not None and
    the nth string in `off_bitarray` is not None, display that string;
    otherwise display nothing.  The displays are collected up from the
    least significant bit and returned separated by a comma and a space,
    in parentheses after the hexadecimal value of the integer."""
    if off_bitarray is None:
        off_bitarray = [ None ] * len(bitarray)
    bits = []
    bitfield = 0
    byte_count = len(bitarray) // 8
    while byte_count > 0:
        bitfield |= data[byte_count-1] << (8 * (byte_count-1))
        byte_count -= 1
    for i in range(len(bitarray)):
        if bitfield & (1 << i):
            bits.append(bitarray[i])
        elif off_bitarray[i] is not None:
            bits.append(off_bitarray[i])
    return ("%%0%dx (%%s)" % (2 * len(bitarray) // 8)) % (bitfield,
                                                          ", ".join(bits))


STATUS = { 0x00: "Success",
           0x01: "Failed",
           0x02: "Invalid Parameter",
           0x09: "Success (no previous item)",
           0x0a: "Initialisation/Deletion Failed",
           0x0c: "Bad Length",
           0x10: "Memory Failure",
           0x11: "Table full",
           0x1a: "Out of resources",
           0xba: "ZApsNotAllowed",
           0xc2: "ZNwkInvalidRequest",
           0xc3: "ZNwkNotPermitted",
           0xc8: "Unknown device",
           0xe9: "ZMacNoAck",
           0xea: "ZMacNoBeacon",
           0xe8: "ZMacInvalidParameter",
           0xfc: "Scan in progress"
}

def field_parse_status(data):
    "Interpret the data as an MTAPI status (ZSTATUS) byte."
    return field_parse_dict(data, STATUS, "Failure(0x%02x)")

LATENCY = { 0x00: "No latency",
            0x01: "Fast beacons",
            0x02: "Slow beacons"
}

def field_parse_latency(data):
    "Interpret the data as a beacon latency byte."
    return field_parse_dict(data, LATENCY, "Invalid(0x%02x)")

OPTIONS = [ "(Reserved)",
            "Wildcard Profile Id",
            "(Reserved)",
            "(Reserved)",
            "APS ACK",
            "Discover Route",
            "APS Security",
            "Skip Routing" ]

def field_parse_options(data):
    "Interpret the data as a network options byte."
    return field_parse_bitfield(data, OPTIONS)

ADDRESS_MODE = { 0x00: "Address not present",
                 0x01: "Group address",
                 0x02: "16-bit address",
                 0x03: "64-bit address",
                 0xff: "Broadcast"
}

def field_parse_address_mode(data):
    "Interpret the data as an address mode byte"
    return field_parse_dict(data, ADDRESS_MODE, "Invalid(0x%02x)")

TX_OPTION = [ "Ack", "GTS", "Indirect", "(Unused)",
              "No Retransmission", "No Confirms",
              "Alternate Backoff Exponent", "Power/Channel"
]

def field_parse_tx_option(data):
    "Interpret the data as a Tx option byte."
    return field_parse_bitfield(data, TX_OPTION)

CAPABILITY_SET = [ "Alternative PAN Coord",
                   "Zigbee Router",
                   "Mains Powered",
                   "Rx On When Idle",
                   "(Reserved)",
                   "(Reserved)",
                   "Security",
                   "Allocate Address"
]
CAPABILITY_UNSET = [ None,
                     "End Device",
                     "Battery Powered",
                     None,
                     None,
                     None,
                     None,
                     None
]

def field_parse_capabilities(data):
    "Interpret the data as a capability byte"
    return field_parse_bitfield(data, CAPABILITY_SET, CAPABILITY_UNSET)

ASSOC_STATUS = { 0x00: "Success",
                 0x01: "PAN at capacity",
                 0x02: "PAN access denied"
}

def field_parse_assoc_status(data):
    "Interpret the data as an association status byte."
    return field_parse_dict(data, ASSOC_STATUS, "Unknown(0x%02x)")

DISASSOC_REASON = { 0x00: "Reserved",
                    0x01: "Coord wishes device to leave",
                    0x02: "Device wishes to leave"
}

def field_parse_disassoc_reason(data):
    "Interpret the data as a disassociation reason code."
    return field_parse_dict(data, DISASSOC_REASON, "Unknown(0x%02x)")

MAC_ATTRIBUTE = { 0x40: "ZMAC_ACK_WAIT_DURATION",
                  0x41: "ZMAC_ASSOCIATION_PERMIT",
                  0x42: "ZMAC_AUTO_REQUEST",
                  0x43: "ZMAC_BATT_LIFE_EXT",
                  0x44: "ZMAC_BATT_LEFT_EXT_PERIODS",
                  0x45: "ZMAC_BEACON_MSDU",
                  0x46: "ZMAC_BEACON_MSDU_LENGTH",
                  0x47: "ZMAC_BEACON_ORDER",
                  0x48: "ZMAC_BEACON_TX_TIME",
                  0x49: "ZMAC_BSN",
                  0x4a: "ZMAC_COORD_EXTENDED_ADDRESS",
                  0x4b: "ZMAC_COORD_SHORT_ADDRESS",
                  0x4c: "ZMAC_DSN",
                  0x4d: "ZMAC_GTS_PERMIT",
                  0x4e: "ZMAC_MAX_CSMA_BACKOFFS",
                  0x4f: "ZMAC_MIN_BE",
                  0x50: "ZMAC_PANID",
                  0x51: "ZMAC_PROMISCUOUS_MODE",
                  0x52: "ZMAC_RX_ON_IDLE",
                  0x53: "ZMAC_SHORT_ADDRESS",
                  0x54: "ZMAC_SUPERFRAME_ORDER",
                  0x55: "ZMAC_TRANSACTION_PERSISTENCE_TIME",
                  0x56: "ZMAC_ASSOCIATED_PAN_COORD",
                  0x57: "ZMAC_MAX_BE",
                  0x58: "ZMAC_FRAME_TOTAL_WAIT_TIME",
                  0x59: "ZMAC_MAC_FRAME_RETRIES",
                  0x5a: "ZMAC_RESPONSE_WAIT_TIME",
                  0x5b: "ZMAC_SYNC_SYMBOL_OFFSET",
                  0x5c: "ZMAC_TIMESTAMP_SUPPORTED",
                  0x5d: "ZMAC_SECURITY_ENABLED",
                  0xe0: "ZMAC_PHY_TRANSMIT_POWER",
                  0xe1: "ZMAC_LOGICAL_CHANNEL",
                  0xe2: "ZMAC_EXTENDED_ADDRESS",
                  0xe3: "ZMAC_ALT_BE"
}

def field_parse_mac_attr(data):
    "Interpret the data as a MAC attribute number."
    return field_parse_dict(data, MAC_ATTRIBUTE, "Unknown(0x%02x)")

SCAN_TYPE = { 0x00: "Energy Detect",
              0x01: "Active",
              0x02: "Passive",
              0x03: "Orphan"
}

def field_parse_scan_type(data):
    "Interpret the data as a scan type."
    return field_parse_dict(data, SCAN_TYPE, "Unknown(0x%02x)")

RESET_TYPE = { 0 : "Hardware", 1: "Software" }
field_parse_reset_type = FieldParseDict(RESET_TYPE, "Unknown(0x%02x)")

RESET_REASON = { 0x00: "Power-up",
                 0x01: "External",
                 0x02: "Watchdog"
}

def field_parse_reset_reason(data):
    "Interpret the data as a reset reason code."
    return field_parse_dict(data, RESET_REASON, "Unknown(0x%02x)")

SYS_CAPABILITIES = [
    "MT_CAP_SYS",
    "MT_CAP_MAC",
    "MT_CAP_NWK",
    "MT_CAP_AF",
    "MT_CAP_ZDO",
    "MT_CAP_SAPI",
    "MT_CAP_UTIL",
    "MT_CAP_DEBUG",
    "MT_CAP_APP",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "MT_CAP_ZOAD",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)"
]

def field_parse_sys_capabilities(data):
    "Interpret the data as a system capabilities byte."
    return field_parse_bitfield(data, SYS_CAPABILITIES)

ADC_CHANNEL = {
    0x00: "AIN0",
    0x01: "AIN1",
    0x02: "AIN2",
    0x03: "AIN3",
    0x04: "AIN4",
    0x05: "AIN5",
    0x06: "AIN6",
    0x07: "AIN7",
    0x0e: "Temperature Sensor",
    0x0f: "Voltage Reading"
}

def field_parse_adc_channel(data):
    "Interpret the data as an ADC channel identifier."
    return field_parse_dict(data, ADC_CHANNEL, "Invalid(0x%02x)")

ADC_RESOLUTION = {
    0x00: "8-bit",
    0x01: "10-bit",
    0x02: "12-bit",
    0x03: "14-bit"
}

def field_parse_adc_resolution(data):
    "Interpret the data as an ADC channel resolution value."
    return field_parse_dict(data, ADC_RESOLUTION, "Invalid(0x%02x)")

GPIO_OP = {
    0x00: "Set direction",
    0x01: "Set input mode",
    0x02: "Set",
    0x03: "Clear",
    0x04: "Toggle",
    0x05: "Read"
}

def field_parse_gpio_operation(data):
    "Interpret the data as a GPIO operation command"
    return field_parse_dict(data, GPIO_OP, "Invalid(0x%02x)")

DEVICE_TYPE = [
    "Coordinator",
    "Router",
    "End Device",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)"
]

def field_parse_device_type(data):
    "Interpret the data as a Zigbee device type"
    return field_parse_bitfield(data, DEVICE_TYPE)

DEVICE_TYPE_AND_INFO = [
    "Coordinator",
    "Router",
    "End Device",
    "Complex Descriptor Available",
    "User Descriptor Available",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)"
]

def field_parse_type_and_info(data):
    "Interpret the data as a combined Zigbee device type and info field."
    return field_parse_bitfield(data, DEVICE_TYPE_AND_INFO)

DEVICE_STATE = {
    0x00: "Unstarted",
    0x01: "Not connected",
    0x02: "Nothing to join",
    0x03: "Joining",
    0x04: "Rejoining",
    0x05: "Unauthenticated",
    0x06: "Authenticated",
    0x07: "Routing",
    0x08: "Starting as Coordinator",
    0x09: "Started as Coordinator",
    0x0a: "Lost Parent Info"
}

def field_parse_device_state(data):
    "Interpret the data as a device state byte."
    return field_parse_dict(data, DEVICE_STATE, "Unknown(0x%02x)")

SUBSYSTEM_ID = {
    0x0100: "MT_SYS",
    0x0200: "MT_MAC",
    0x0300: "MT_NWK",
    0x0400: "MT_AF",
    0x0500: "MT_ZDO",
    0x0600: "MT_SAPI",
    0x0700: "MT_UTIL",
    0x0800: "MT_DEBUG",
    0x0900: "MT_APP",
    0xffff: "ALL_SUBSYSTEMS"
}

def field_parse_subsystem_id(data):
    "Interpret the data as an MTAPI subsystem ID"
    return field_parse_dict(data, SUBSYSTEM_ID, "Reserved(0x%04x)")

DISABLE_ENABLE = { 0: "Disable", 1: "Enable" }

def field_parse_enable(data):
    "Interpret the data as a boolean Disable/Enable field"
    return field_parse_dict(data, DISABLE_ENABLE, "Unexpected(0x%02x)")

KEYS = ["Key 1", "Key 2", "Key 3", "Key 4",
        "Key 5", "Key 6", "Key 7", "Key 8"
]

def field_parse_keys(data):
    "Interpret the data as a keycode (for Dev Board button presses)"
    return field_parse_bitfield(data, KEYS)

SHIFT = { 0: "No shift", 1: "Shift" }

def field_parse_shift(data):
    "Interpret the data as a boolean Shift Key field"
    return field_parse_dict(data, SHIFT, "Unexpected(0x%02x)")

ON_OFF = { 0: "OFF", 1: "ON" }

def field_parse_onoff(data):
    "Interpret the data as a boolean On/Off field"
    return field_parse_dict(data, ON_OFF, "Unexpected(0x%02x)")

RELATION = {
    0: "Parent",
    1: "Child RFD",
    2: "Child RFD RxIdle",
    3: "Child FFD",
    4: "Child FFD RxIdle",
    5: "Neighbour",
    6: "Other"
}

def field_parse_relation(data):
    "Interpret the data as a relationship."
    return field_parse_dict(data, RELATION, "Invalid(0x%02x)")

LEAVE_ACTION = [
    "Rejoin",
    "Remove Children",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)",
    "(Reserved)"
]

def field_parse_leave_action(data):
    "Interpret the data as a leave action code"
    return field_parse_bitfield(data, LEAVE_ACTION)

STARTUP_STATUS = {
    0: "Restored network state",
    1: "New network state",
    2: "Leave and not Started"
}

def field_parse_startup_status(data):
    "Interpret the data as a startup status byte"
    return field_parse_dict(data, STARTUP_STATUS, "Unexpected(0x%02x)")

SERVER_MASK = [
    "Primary Trust Centre",
    "Backup Trust Centre",
    "Primary Binding Table Cache",
    "Backup Binding Table Cache",
    "Primary Discovery Cache",
    "Backup Discovery Cache",
    "(Reserved)",
    "(Reserved)"
]

def field_parse_server_mask(data):
    "Interpret the data as a server capability mask."
    return field_parse_bitfield(data, SERVER_MASK)

ROUTING_STATUS = {
    0x00: "Active",
    0x01: "Discovery Underway",
    0x02: "Discovery Failed",
    0x03: "Inactive"
}

def field_parse_routing_status(data):
    "Interpret the data as a routing status byte."
    return field_parse_dict(data, ROUTING_STATUS, "Invalid(0x%02x)")

JOIN_DURATION = {
    0x00: "Disabled",
    0xff: "Enabled"
}

def field_parse_join_duration(data):
    "Interpret the data as a join duration byte."
    return field_parse_dict(data, JOIN_DURATION, "0x%02x")
