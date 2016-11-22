import argparse
import logging
import time

import pogo.util as util
from pogo.api import PokeAuthSession
from pogo.custom_exceptions import GeneralPogoException
from pogo.trainer import Trainer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def api(request):
    if request.POST:

        if request.POST['auth'] not in ['ptc', 'google']:
            raise GeneralPogoException(
                'Invalid auth service {}'.format(args.auth))

        auth_session = PokeAuthSession(
            request.POST['username'],
            request.POST['password'],
            request.POST['auth'],
        )

        session = auth_session.authenticate()

        if session:
            trainer = Trainer(auth_session, session)
            time.sleep(1)
            profile_data = trainer.session.getProfile()
            inventory_data = str(trainer.session.inventory)
            return HttpResponse(inventory_data, content_type='text/plain')
        else:
            logging.critical('Session not created successfully')
