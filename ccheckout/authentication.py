import httplib, urllib, base64, json, sys

class AuthError(Exception):
    def __init__(self):
         self.msg = "auth error"

    # read the oauth secrets and account ID from a configuration file
    def loadSecret():
        # read the s3 creds from json file
        try:
             credsFile=open('secrets.txt')
             creds = json.load(credsFile)
             return creds
        except Exception as e:
            print("Error loading oauth secret from local file called 'brightcove_oauth.txt'")
            sys.exit("System error: " + str(e) )

    # get the oauth 2.0 token
    
    def getAuthToken(creds):
        conn = httplib.HTTPSConnection("oauth.brightcove.com")
        url =  "/v4/access_token"
        params = {
             "grant_type": "client_credentials"
             }
        client = creds["client_id"]
        client_secret = creds["client_secret"]
        authString = base64.encodestring('%s:%s' % (client, client_secret)).replace('\n', '')
        requestUrl = url + "?" + urllib.urlencode(params)
        headersMap = {
             "Content-Type": "application/x-www-form-urlencoded",
             "Authorization": "Basic " + authString
             }
        conn.request("POST", requestUrl, headers=headersMap)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            result = json.loads( data )
        return result["access_token"]
    
    def createPaymentCardsJSON():
      url = "https://tropipay-dev.herokuapp.com/api/v2/paymentcards"
      
      payload = {
            "reference": "Cobosis",
            "concept": "Producto",
            "favorite": True,
            "description": "Producto de aseo",
            "amount": 5000,
            "currency": "USD",
            "singleUse": True,
            "reasonId": 4,
            "expirationDays": 1,
            "lang": "es",
            "urlSuccess": "http://127.0.0.1:8000/compra/exito/",
            "urlFailed": "http://127.0.0.1:8000/compra/fallo/",
            "urlNotification": "https://webhook.site/0c8da2ed-ce2a-4f72-9de1-905b662e1e22",
            "serviceDate": "2024-04-30",
            "client": {
                  "name": "Yuniesky",
                  "lastName": "Coca",
                  "address": "Saldo. 8 A Interior, El Cerro, La Habana",
                  "phone": "+5358236469",
                  "email": "ycocab@gmail.com",
                  "countryId": 3,
                  "termsAndConditions": "true"
                  },
                  "directPayment": True,
                  "paymentMethods": ["EXT", "TPP"]
                  }
      headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODI3LCJjcmVkZW50aWFsTmFtZSI6IjU2ODRhNTU0YzMyOWFhOTk5ZDY2MzY5N2U4ZDM0MDRhIiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ0ODczMDQsImV4cCI6MTcxNDQ5NDUwNH0.Qv2rya0EC4MItnYwo08Qz9pavgXOMBYglYMeU-zzgUQ",
            "Prefer": "code=200, example=Example with client data",
            "Content-Type": "application/json",
            "Accept": "application/json"
            }
      

    # call Analytics API for video views in the last 30 days
    def getVideoViews( token , account ):
        conn = httplib.HTTPSConnection("data.brightcove.com")
        url =  "/analytics-api/videocloud/account/" + account + "/report/"
        params = {
             "dimensions": "video",
             "limit": "10",
             "sort": "video_view",
             "fields": "video,video_name,video_view",
             "format": "json"
             }
        requestUrl = url + "?" + urllib.urlencode(params)
        headersMap = {
             "Authorization": "Bearer " + token
             }
        conn.request("POST", requestUrl, headers=headersMap)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            result = json.loads( data )
            return result
        elif response.status == 401:
            # if we get a 401 it is most likely because the token is expired.
            raise AuthError
        else:
            raise Exception('API_CALL_ERROR' + " error " + str(response.status) )
        # call CMS API to return the number of videos in the catalog
    
    def getVideos( token , account ):
        conn = httplib.HTTPSConnection("cms.api.brightcove.com")
        url =  "/v1/accounts/" + account + "/counts/videos/"
        requestUrl = url
        print "GET " + requestUrl
        headersMap = {
             "Authorization": "Bearer " + token
             }
        conn.request("GET", requestUrl, headers=headersMap)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            result = json.loads( data )
            return result
        elif response.status == 401:
            # if we get a 401 it is most likely because the token is expired.
            raise AuthError
        else:
            raise Exception('API_CALL_ERROR' + " error " + str(response.status) )

    def demo():
        creds = loadSecret()
        token = getAuthToken(creds)
        account = creds["account"];
        try:
            results = getVideos( token , account )
        except AuthError, e:
            # handle an auth error by re-fetching a auth token again
            token = getAuthToken(creds)
            results = getVideoViews( token , account )
            # print the videos
            print(results)
        if __name__ == "__main__":
            demo()