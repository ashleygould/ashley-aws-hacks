#!/bin/env python

import sys
from sceptre.cli import setup_logging
from sceptremods.hooks.acm_certificate import AcmCertificate

request = AcmCertificate(argument=' '.join(sys.argv[1:]))
request.logger = setup_logging(True, False)
request.run()

