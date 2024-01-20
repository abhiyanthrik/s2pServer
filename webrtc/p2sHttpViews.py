import asyncio
import json
from av import VideoFrame
import logging
import time
import os
from django.http import HttpResponse
from django.shortcuts import render
import json
from webrtc import customVideoTrack
from aiortc import (
    MediaStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    RTCConfiguration,
    RTCIceServer,
)
from aiortc.contrib.media import MediaRelay
from webrtc.RTCPeer import RTCPeer
from django.views.decorators.csrf import csrf_exempt

ROOT = os.path.dirname(__file__)
logger = logging.getLogger("pc")
pc = RTCPeerConnection()
relay = MediaRelay()


async def p2sHttpIndex(request):
    return render(request, "./p2sHttp.html")


@csrf_exempt
async def offer(request):
    params = json.loads(request.body)
    con = RTCPeer()
    res = await con.handle(params=params)
    return HttpResponse(res)
