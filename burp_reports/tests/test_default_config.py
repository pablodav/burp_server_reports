from ..defaults.default_config import set_defaults


def test_default_config():
    config = set_defaults()
    assert config['inventory_status']['active'] == 'active'
