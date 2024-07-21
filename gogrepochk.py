"""gogrepochk.py

Module that check for GOG's offline resources updates.

This module gather GOG offline resources info from given dir while tracking
for update status from www.gogdb.org. The given dir must be organized in the
form of GGGSS aka General GOG-Game Saving Scheme.

Scratched by t0nkov.
Version: 0.0
"""

import os  
import requests
import json

_gogdbapi = 'https://www.gogdb.org/data/products/%s/product.json'

def getProductData(api: str, id: str) -> dict:
    """Get product data from given api, returns in dict form.
    
    Args:
            api:    String of api with a format operator (%s).
            id:     String of product (Game/DLC) id.
    """
    pageurl = api % id
    sess = requests.sessions.Session()
    resp = sess.get(pageurl)
    if resp.status_code == 404:
        raise ValueError('Unknown id [%s]' % id)
    return json.loads(resp.text)

def clearDirStr(strin: str) -> str:
    forbidden_chars = r'\/:*?"<>|'
    for char in forbidden_chars:
        strin.replace(char, '_')
    return strin

class Product:
    """Defines a general product class."""
    def __init__(self, path: str, dir: str):
        """
        Args:
            path:   Path string to the product location (game/dlc).
                    e.g.
                        'D:/MyGOGcollection/'
                        'D:/MyGOGcollection/game_of_mine`103453456/`dlc/'
            dir:    String of the product's dir name.
                    e.g.
                        'game_of_mine`103453456'
                        'gom_epispde_1`108937456'
        """
        self.slug, self.id = dir.split('`')
        self.path = os.path.join(path, dir)

        self.have_installer = False
        self.repo_version_win = set()
        self.repo_version_linux = set()
        self.repo_version_osx = set()

        self.online_version_win = set()
        self.online_version_linux = set()
        self.online_version_osx = set()

        dirlist = os.listdir(self.path)
        for dirname in dirlist:
            if dirname[0] != '`':
                self.have_installer = True

                if dirname[-4:] == '`win':
                    self.repo_version_win.add(dirname)
                elif dirname[-6:] == '`linux':
                    self.repo_version_linux.add(dirname)
                elif dirname[-4:] == '`osx':
                    self.repo_version_osx.add(dirname)
                else:
                    raise ValueError('Unknown version-platform [%s] for [%s]' %
                                     (dirname, self.slug))
        self.updatechk(_gogdbapi)

        

    def updatechk(self, api: str):
        """Update self parameters using given api.

        Args:
        api:    String of api with a format operator (%s).
        """
        if not self.have_installer:
            self.have_win_update = False
            self.have_linux_update = False
            self.have_osx_update = False
            self.have_update = False
        else:
            datadict = getProductData(api, self.id)
            if self.slug != datadict['slug']:
                raise ValueError('Unmatching id [%s] for product [%s]' %
                                 (self.id, self.slug))
            installer_list = datadict['dl_installer']  

            for entity in installer_list:
                if entity['version'] == None:
                    versionstr = '_'
                else:
                    versionstr = clearDirStr(entity['version'])

                if entity['os'] == 'windows':
                    self.online_version_win.add('%s`win' % versionstr)
                elif entity['os'] == 'linux':
                    self.online_version_linux.add('%s`linux' % versionstr)
                elif entity['os'] == 'osx':
                    self.online_version_osx.add('%s`osx' % versionstr)

            for version_string in self.repo_version_win:
                self.online_version_win.discard(version_string)
            for version_string in self.repo_version_linux:
                self.online_version_linux.discard(version_string)
            for version_string in self.repo_version_osx:
                self.online_version_osx.discard(version_string)

            if len(self.repo_version_win) == 0:
                self.have_win_update = False
            elif len(self.online_version_win) == 0:
                self.have_win_update = False
            else:
                self.have_win_update = True
            
            if len(self.repo_version_linux) == 0:
                self.have_linux_update = False
            elif len(self.online_version_linux) == 0:
                self.have_linux_update = False
            else:
                self.have_linux_update = True

            if len(self.repo_version_osx) == 0:
                self.have_osx_update = False
            elif len(self.online_version_osx) == 0:
                self.have_osx_update = False
            else:
                self.have_osx_update = True
            self.have_update = (self.have_win_update or self.have_linux_update
                                or self.have_osx_update)

class DLC(Product):
    """Defines GGGSS DLC class."""
    pass

class Title(Product):
    """Defines GGGSS Title class."""
    def __init__(self, title_loc: str, dir: str):
        """
        Args:
            title_loc:  Location of the title.
                        e.g.
                            'D:/MyGOGcollection'
            dir:        String of the title's dir.
                        e.g.
                            'game_of_mine`102943556'
        """
        super().__init__(title_loc, dir)
        self.dlclist = []
        dlcpath = os.path.join(self.path, '`dlc')
        if os.path.isdir(dlcpath):
            for dlcdir in os.listdir(dlcpath):
                if dlcdir[0] == '`':
                    continue
                print('    Find dlc [%s]' % dlcdir)
                self.dlclist.append(DLC(dlcpath, dlcdir))

class Repo:
    """Defines GGGSS Repo class. Checks for updates upon init process."""
    def __init__(self, repopath: str):
        """
        Args:
            repopath:   Path to the GOG game repo.
                        e.g.
                            'D:/MyGOGcollection'
        """
        self.titlelist = []
        for titledir in os.listdir(repopath):
            if titledir[0] == '`':
                continue
            print('Find title [%s]' % titledir)
            self.titlelist.append(Title(repopath, titledir))
    
    def printUpdates(self):
        for title in self.titlelist:
            if title.have_update:
                print('%s %s' % (title.slug, title.id))
                if title.have_win_update:
                    print('    Win:   %s' % title.online_version_win)
                if title.have_linux_update:
                    print('    Linux: %s' % title.online_version_linux)
                if title.have_osx_update:
                    print('    OSX:   %s' % title.online_version_osx)
            have_print_title = title.have_update
            for dlc in title.dlclist:
                if dlc.have_update:
                    if not have_print_title:
                        print('%s %s' % (title.slug, title.id))
                        have_print_title = True
                    print('    %s %s' % (dlc.slug, dlc.id))
                    if dlc.have_win_update:
                        print('        Win:   %s' % dlc.online_version_win)
                    if dlc.have_linux_update:
                        print('        Linux: %s' % dlc.online_version_linux)
                    if dlc.have_osx_update:
                        print('        OSX:   %s' % dlc.online_version_osx)


if __name__ == '__main__':
    repo = Repo(r'E:/gog-repo')
    print()
    repo.printUpdates()
