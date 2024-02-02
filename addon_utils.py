import bpy

def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)

def safe_poll(poll_function):
    def safe_poll_function(cls, context):
        try:
            return poll_function(cls, context)
        except AttributeError:
            return False
    
    return classmethod(safe_poll_function)