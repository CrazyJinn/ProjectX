
def format_interface_name(interface_name):
    interface_mapping = {
        'ShoppingOrder/SplitOrder'.lower(): 'shopping/splitorder',
        'ShoppingOrder/MatchItem'.lower(): 'shopping/MatchItem',
        'Shipping/SetShippingInfo'.lower(): 'shipping/set'
    }
    interface_name = interface_name.lower()
    result = interface_mapping.get(interface_name)
    if result != None:
        return result
    else:
        return interface_name
