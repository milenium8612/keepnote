"""

    KeepNote    
    
    Low-level Create-Read-Update-Delete (CRUD) interface for notebooks.

"""

#
#  KeepNote
#  Copyright (c) 2008-2011 Matt Rasmussen
#  Author: Matt Rasmussen <rasmus@mit.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
#


#=============================================================================
# errors


class ConnectionError (StandardError):
    def __init__(self, msg, error=None):
        StandardError.__init__(self, msg)
        self.error = error

    def repr(self):
        if self.error is not None:
            return StandardError.repr(self) + ": " + repr(self.error)
        else:
            return StandardError.repr(self)

class UnknownNode (ConnectionError):
    def __init__(self, msg="unknown node"):
        ConnectionError.__init__(self, msg)

class NodeExists (ConnectionError):
    def __init__(self, msg="node exists"):
        ConnectionError.__init__(self, msg)

class UnknownFile (ConnectionError):
    def __init__(self, msg="unknown file"):
        ConnectionError.__init__(self, msg)

class CorruptIndex (ConnectionError):
    def __init__(self, msg="index error", error=None):
        ConnectionError.__init__(self, msg, error)


#=============================================================================


def path_join(*parts):
    """
    Join path parts for node file paths

    Node files always use '/' for path separator.
    """
    # skip initial empty strings
    i = 0
    while parts[i] == "":
        i +=1
    return "/".join(parts[i:])


def path_basename(filename):
    """
    Return the last component of a filename

    aaa/bbb   =>  bbb
    aaa/bbb/  =>  bbb
    aaa/      =>  aaa
    aaa       =>  aaa
    ''        =>  ''
    /         =>  ''
    """

    if filename.endswith("/"):
        i = filename.rfind("/", 0, -1) + 1
        return filename[i:-1]
    else:
        i = filename.rfind("/", 0, -1) + 1
        return filename[i:]



#=============================================================================

class NoteBookConnection (object):
    def __init__(self):
        pass

    #================================
    # Filesystem-specific API (may not be supported by some connections)
    
    def get_node_path(self, nodeid):
        """Returns the path of the node"""
        pass
    
    def get_node_basename(self, nodeid):
        """Returns the basename of the node"""
        pass

    #======================
    # connection API

    def connect(self, filename):
        """Make a new connection"""
        pass
        
    def close(self):
        """Close connection"""
        pass

    def save(self):
        """Save any unsynced state"""
        pass

    #======================
    # Node I/O API

    def create_root(self, nodeid, attr):
        """Create the root node"""
        pass

    def create_node(self, nodeid, attr):
        """Create a node"""
        pass
        
    def read_root(self):
        """Read root node attr"""
        pass
    
    def read_node(self, nodeid):
        """Read a node attr"""
        pass

    def update_node(self, nodeid, attr):
        """Write node attr"""
        pass

    def delete_node(self, nodeid):
        """Delete node"""
        pass

    def has_node(self, nodeid):
        return False

    # secondary node API (try to simplify)
    
    def read_data_as_plain_text(self, nodeid):
        """Iterates over the lines of the data file as plain text"""
        pass

    # TODO: try remove concept of parentids and childids from connection API

    def get_rootid(self):
        """Returns nodeid of notebook root node"""
        pass

    def get_parentid(self, nodeid):
        """Returns nodeid of parent of node"""
        pass
    
    def list_children_attr(self, nodeid):
        """List attr of children nodes of nodeid"""
        pass

    def list_children_nodeids(self, nodeid):
        """List nodeids of children of node"""
        pass


    #===============
    # file API

    def open_file(self, nodeid, filename, mode="r", 
                        codec=None):
        """Open a file contained within a node"""        
        pass

    def delete_file(self, nodeid, filename, _path=None):
        """Open a file contained within a node"""
        pass

    # Is this needed inside the connection?  Can it be support outside?
    def new_filename(self, nodeid, new_filename, ext=u"", sep=u" ", number=2, 
                     return_number=False, use_number=False, ensure_valid=True):
        pass

    def mkdir(self, nodeid, filename):
        pass

    def list_files(self, nodeid, filename=None):
        """
        List data files in node
        """
        pass
    
    def file_exists(self, nodeid, filename):
        pass

    def file_basename(self, filename):
        pass
                
    def copy_file(self, nodeid1, filename1, nodeid2, filename2):
        """
        Copy a file between two nodes

        if node is None, filename is assumed to be a local file
        """
        pass


    def copy_files(self, nodeid1, nodeid2):
        """
        Copy all data files from nodeid1 to nodeid2
        """
        pass


    # TODO: returning a fullpath to a file is not fully portable
    # will eventually need some kind of fetching mechanism
    
    def get_file(self, nodeid, filename, _path=None):
        pass


    #---------------------------------
    # index management

    def init_index(self):
        """Initialize the index"""
        pass
    
    def index_needed(self):
        pass

    def clear_index(self):
        pass

    def index_all(self):
        pass


    #---------------------------------
    # indexing/querying

    def index_attr(self, key, index_value=False):
        """Add indexing for an attribute"""
        pass

    def search_node_titles(self, text):
        """Search nodes by title"""
        pass

    def search_node_contents(self, text):
        """Search nodes by content"""
        pass

    def has_fulltext_search(self):
        pass

    def update_index_node(self, nodeid, attr):
        """Update a node in the index"""
        pass
    
    def get_node_path_by_id(self, nodeid):
        """Lookup node path by nodeid"""
        pass

    def get_attr_by_id(self, nodeid, key):
        pass





# TODO: need to keep namespace of files and node directories spearate.
# Need to carefully define what valid filenames look like.
#  - is it case-sensitive?
#  - which characters are allowed?
#  - would do a translation between what the user thinks the path is and
#    what is actually used on disk.


"""
File path translation strategy.

on disk            user-visible
filename      =>     filename
__filename    =>     filename
____filename  =>     __filename

user-visble       on disk 
filename      =>  filename (if simple file exists)
              =>  __filename (if simple file does not-exist)
__filename    =>  ____filename


Within an attached directory naming scheme is 1-to-1



Reading filename from disk:
  filename = read_from_disk()
  if filename.startswith("__"):
    # unquote filename
    return filename[2:]

Looking for filename on disk:
  if filename.startswith("__"):
    # escape '__'
    filename = "__" + filename
  if simple_file_exists(filename):  # i.e. not a node dir
    return filename
  else:
    # try quoted name
    return "__" + filename


node directories aren't allowed to start with '__'.

"""
