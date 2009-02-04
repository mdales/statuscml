# The MIT License
#
# Copyright (c) 2009 Cambridge Visual Networks Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
# We create the PingdomAPI modules using 
#  wsdl2py -u https://ws.pingdom.com/soap/PingdomAPI.wsdl
from PingdomAPI_services import *

def index(request):
    return HttpResponse("Hello World!")
    
def statuscml(request):
    import time

    width = request.GET.get('width', 1280)
    height = request.GET.get('height', 1024)

    # Get a connection to the server
    pal = PingdomAPILocator()
    portType = pal.getPingdomAPISoapPort()

    # Authenticate
    username = 'blah@blah.blah'
    passwd = 'blah'
    apikey = 'blahblahblahblahblahblah'

    class authCredentials: 
        pass
    authinfo = login_input()
    authinfo._APIKey = apikey
    ac = authCredentials()
    ac._username = username
    ac._password = passwd
    authinfo._credentialsData = ac
    login_resp = portType.Auth_login( authinfo)
    sessionId = login_resp._return._sessionId
    # Logged in

    # Let's get the current states of all the checks
    rgcsi = get_current_states_input()
    rgcsi._APIKey = apikey
    rgcsi._sessionId = sessionId

    checkStates = [
        (s._checkName, s._checkState, 
            time.strftime("%H:%M on %a %b %d", time.gmtime(time.mktime(s._lastCheckTime))))
            for s in portType.Report_getCurrentStates(rgcsi)._return._currentStates
        ]

    return render_to_response('statuscml.html', 
            {'checkstates': checkStates, 'width': width, 'height':height}
            )

