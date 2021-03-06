from .. import log; log = log[__name__]

from os.path import basename, exists, isfile, isdir, join as pjoin

import fnmatch
import re

from pyramid.traversal import traverse
from pyramid.url import static_url

import ROOT as R

from ..locationaware import LocationAware
from ..multitraverser import MultipleTraverser
from ..actions import action
from .util import get_key_class
from .object import RootObject
from .builder import build_root_object


class RootFileTraverser(LocationAware):
    """
    A traverser to go across ROOT files
    """
    section = "root_file"
    
    def __init__(self, request, rootfile):
        self.request, self.rootfile = request, rootfile
    
    @property
    def name(self):
        return basename(self.rootfile.GetName())
        
    @property
    def icon_url(self):
        return static_url('weboot:static/folder_chart_32.png', self.request)
        
    @property
    def path(self):
        return self.rootfile.GetPath()
        
    @property
    def content(self):
        keys = [k.GetName() for k in self.rootfile.GetListOfKeys()]
        def link(p):
            url = self.request.resource_url(self, p)
            return '<p><a href="{0}">{1}</a><img src="{0}/render?resolution=25" height="10%"/></p>'.format(url, p)
        return "".join(link(p) for p in keys)
    
    def keys(self):
        return sorted(k.GetName() for k in self.rootfile.GetListOfKeys())
    
    def __iter__(self):
        return iter(self.keys())
    
    @property
    def items(self):
        keys = [self[k.GetName()] for k in self.rootfile.GetListOfKeys()]
        keys = [k for k in keys if k]
        keys.sort(key=lambda k: k.name)
        return keys
    
    @action
    def basket(self, parent, key):
        if not self.request.db:
            raise HTTPMethodNotAllowed("baskets not available - no connect to database")
        else:
            self.request.db.baskets.insert({"basket":"my_basket",
                "path": resource_path(self), "name": self.name})
            log.debug("adding {0} to basket".format(self.url))
            return HTTPFound(location=self.url)
        
    @action
    def selectclass(self, parent, key, cls):
        raise NotImplementedError("This should be re-implemented if it is needed")
    
    def __getitem__(self, key):
        log.debug("Traversing root object at '{0}'".format(key))
        
        if MultipleTraverser.should_multitraverse(key):
            return MultipleTraverser.from_listable(self, key)
            
        leaf = self.rootfile.GetKey(key)
        if not leaf:
            return
            
        leaf_cls = get_key_class(leaf)
        log.debug("-- {0} {1} {2}".format(self.rootfile, key, leaf.GetClassName()))
                
        if not leaf or not leaf_cls:
            return
            
        if issubclass(leaf_cls, R.TDirectory):
            leaf = self.rootfile.Get(key)
            return RootFileTraverser.from_parent(self, key, leaf)
        
        if issubclass(leaf_cls, R.TObjArray):
            leaf = self.rootfile.Get(key)
            return TObjArrayTraverser.from_parent(self, key, leaf)
        
        return build_root_object(self, key, leaf)

