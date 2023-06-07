# QualysAPI module


### _class_ QualysAPI.QualysAPI(svr='', usr='', passwd='', proxy='', enableProxy=False, debug=False)
Bases: `object`

Class to simplify the making and handling of API calls to the Qualys platform

## Class Members

server          : String  : The FQDN of the API server (with [https://](https://) prefix)
user            : String  : The username of an API user in the subscription
password        : String  : The password of the API user
proxy           : String  : The FQDN of the proxy server to be used for connections (with [https://](https://) prefix)
debug           : Boolean : If True, will output debug information to the console during member function execution
enableProxy     : Boolean : If True will force connections via the proxy defined in the ‘proxy’ class member
callCount       : Integer : The number of API calls made during the life of the API object

## Class Methods

__init__(svr, usr, passwd, proxy, enableProxy, debug)

> Called when an object of type QualysAPI is created

> > svr

> >     Default value = “”

> > usr

> >     Default value = “”

> > passwd

> >     Default value = “”

> > proxy

> >     Default value = “”

> > enableProxy

> >     member
> >     Default value = False

> > debug

> >     execution
> >     Default value = False

podPicker(pod)

> Convert a POD string to an API URL

> > pod

> >     ‘AE01’, ‘AU01’, ‘CA01’ or ‘IN01’)

makeCall(url, payload, headers, retryCount)

> Make a Qualys API call and return the response in XML format as an ElementTree.Element object

> > url

> >     NO DEFAULT VALUE, REQUIRED PARAMETER

> > payload

> >     Default value = “”

> > headers

> >     Default value = None

> > retryCount

> >     limit handling, not intended for use by users
> >     Default value = 0

> Example :

>     api = QualysAPI(svr=’[https://qualysapi.qualys.com](https://qualysapi.qualys.com)’,

>         usr=’username’,
>         passwd=’password’,
>         proxy=’[https://proxy.internal](https://proxy.internal)’,
>         enableProxy = True,
>         debug=False)

>     fullurl = ‘%s/full/path/to/api/call’ % api.url

>     api.makeCall(url=fullURL, payload=’’, headers={‘X-Requested-With’: ‘python3’})


#### \__init__(svr='', usr='', passwd='', proxy='', enableProxy=False, debug=False)

#### callCount(_: in_ )

#### debug(_: boo_ )

#### enableProxy(_: boo_ )

#### headers(_ = {_ )

#### makeCall(url, payload='', headers=None, retryCount=0, method='POST', returnwith='xml')

#### password(_: st_ )

#### podPicker()

#### proxy(_: st_ )

#### server(_: st_ )

#### sess(_: Sessio_ )

#### user(_: st_ )
