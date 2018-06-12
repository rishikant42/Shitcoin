# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii
from collections import OrderedDict

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class Home(View):
    template_name = 'home.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

class Index(View):
    template_name = 'index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

class NewWallet(View):
    template_name = 'index.html'
    def get(self, request):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        response = {
                'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
                'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
                }

        return JsonResponse(response)
        # return render(request, self.template_name, context=response)

class MakeTransaction(View):
    template_name = 'make_transaction.html'

    def get(self, request):
        return render(request, self.template_name)

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'recipient_address': self.recipient_address,
                            'value': self.value})

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


class GenerateTransaction(View):
    template_name = 'make_transaction.html'

    def post(self, request):
        sender_address = request.POST['sender_address']
        sender_private_key = request.POST['sender_private_key']
        recipient_address = request.POST['recipient_address']
        value = request.POST['amount']

        transaction = Transaction(sender_address, sender_private_key, recipient_address, value)

        response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}

        return JsonResponse(response)

@csrf_exempt
def generate_txn(request):
    sender_address = request.POST['sender_address']
    sender_private_key = request.POST['sender_private_key']
    recipient_address = request.POST['recipient_address']
    value = request.POST['amount']

    transaction = Transaction(sender_address, sender_private_key, recipient_address, value)

    response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}

    return JsonResponse(response)
