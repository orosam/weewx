try:
    from os import getgid
    from grp import getgrgid
 
    def get_groupname():
        return getgrgid(getgid()).gr_name

except ImportError:
    def get_groupname():
        return "nobody"
