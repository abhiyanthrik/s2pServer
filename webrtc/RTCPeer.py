import asyncio
import json
from av import VideoFrame
import logging
import time
from asgiref.sync import async_to_sync

# import cv2
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


class RTCPeer:
    def __init__(self) -> None:
        pass

    async def handle(self, params) -> HttpResponse:
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        ice_server = RTCIceServer(
            urls=["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"]
        )
        configuration = RTCConfiguration(iceServers=[ice_server])

        pc = RTCPeerConnection(configuration=configuration)
        transciever = pc.addTransceiver(trackOrKind="video", direction="sendrecv")
        local_video = customVideoTrack.CustomVideoTrack(params["framerate"])
        transciever.sender.replaceTrack(local_video)

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(m):
                print("data channel: " + m)
                channel.send("server = " + m)

        @pc.on("track")
        def on_track(track):
            pass
            # pc.addTrack(track)
            # local_video = rtspOut("rtsp://192.168.214.72:1935")
            # local_video = rtspOut(track)
            # local_video = pureRtspOut(useDefaultFrameRate=False, framerate=15)
            # local_video = customVideoTrack.CustomVideoTrack(1)
            # pc.addTrack(local_video)

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        start_time = time.time()
        await pc.setLocalDescription(answer)
        print("--- %s seconds ---" % (time.time() - start_time))

        return HttpResponse(
            json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )
