# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

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

class Wallet(View):
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
