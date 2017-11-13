from datetime import datetime
import os

from cafe.common.reporting import cclogging
from cafe.configurator.managers import TestEnvManager
from cafe.drivers.unittest.runner import UnittestRunner


def before_all(context):
    userdata = context.config.userdata
    if userdata.get('cafe_proj') and userdata.get('cafe_config'):
        cafe_proj = userdata.get('cafe_proj')
        cafe_proj = userdata.get('cafe_config')
        # test_repo_package_name isn't actually necessary for this code path,
        # just adding a valid package path for the sake of this example
        test_env = TestEnvManager(
            userdata.get('cafe_proj'),
            userdata.get('cafe_config') + '.config',
            test_repo_package_name='cafe')
        test_env.finalize()
        cclogging.init_root_log_handler()
        UnittestRunner.print_mug_and_paths(test_env)


def before_feature(context, feature):
    context.log = cclogging.getLogger('')
    log_handler = cclogging.setup_new_cchandler(feature.name)
    context.log.addHandler(log_handler)
    cclogging.log_info_block(context.log,
        [('Feature', feature.name),
         ('Started At', datetime.now())])


def after_feature(context, feature):
    cclogging.log_info_block(context.log,
        [('Feature', feature.name),
         ('Result', feature.status),
         ('Elapsed Time', feature.duration),
         ('Ended At', datetime.now())])