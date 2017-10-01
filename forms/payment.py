"""Method to send payment."""
import json
import urllib2


def make_payment(premium):
    """Method to make payments."""
    try:
        amount = str(int(premium) * 100)
        url_parts = 'KenswitchMobile/webresources/dits/fundstransfer'
        url = 'http://41.215.139.59:8086/' + url_parts

        data = {"custid": "5B03-7321-93E9-4FED",
                "ttype": "t2a",
                "bankcode": "66",
                "acc": "01001030021701",
                "amt": amount,
                "pcode": "1234",
                "qualifier": "0"
                }
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        rjson = json.dumps(data)
        response = urllib2.urlopen(req, rjson)
        message = response.read()

        resp = json.loads(message)
    except Exception, e:
        print "Error making payment - %s" % (str(e))
        return {}
    else:
        return resp


if __name__ == '__main__':
    res = make_payment(12)
    print res
