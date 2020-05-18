from CTFd.plugins.flags import BaseFlag, FLAG_CLASSES
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.user import get_current_user
from CTFd.plugins.address_flag import web3utils

class AddressFlag(BaseFlag):
    name = "address"
    templates = {
        "create": "/plugins/address_flag/assets/address/create.html",
        "update": "/plugins/address_flag/assets/address/edit.html",
    }

    @staticmethod
    def compare(chal_key_obj, provided):
        # chal_key_obj.content      address of the contract
        # provided                  transaction hash

        user_obj = get_current_user()
        assigned_content = user_obj.email
        return web3utils.verify(chal_key_obj.content, assigned_content, provided)

def load(app):
    FLAG_CLASSES["address"] = AddressFlag
    register_plugin_assets_directory(app, base_path="/plugins/address_flag/assets/")
