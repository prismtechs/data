from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .ccavutil import decrypt,encrypt
from .ccavResponseHandler import res
from string import Template

# Your access code and working key
accessCode = 'AVOO30KK42AQ22OOQA'
workingKey = 'B9924C2160DF36BB91F30C6065758B86'


def webprint(request):
    return render(request, 'dataFrom.htm')

@csrf_exempt
def ccavResponseHandler(request):
    if request.method == 'POST':
        plainText = res(request.POST.get('encResp', ''))
        return HttpResponse(plainText)
    return HttpResponse("Invalid Request")

@csrf_exempt
def ccavRequestHandler(request):
    if request.method == 'POST':
        # Extracting form data from POST request
        form_data = {
            'merchant_id': request.POST.get('merchant_id', ''),
            'order_id': request.POST.get('order_id', ''),
            'currency':request.POST.get('currency',''),
            'amount' : request.POST.get('amount',''),
            'redirect_url' : request.POST.get('redirect_url',''),
            'cancel_url' : request.POST.get('cancel_url',''),
            'language' : request.POST.get('language',''),
            'billing_name' : request.POST.get('billing_name',''),
            'billing_address' : request.POST.get('billing_address',''),
            'billing_city' : request.POST.get('billing_city',''),
            'billing_state' : request.POST.get('billing_state',''),
            'billing_zip' : request.POST.get('billing_zip',''),
            'billing_country' : request.POST.get('billing_country',''),
            'billing_tel' : request.POST.get('billing_tel',''),
            'billing_email' : request.POST.get('billing_email',''),
            'delivery_name' : request.POST.get('delivery_name',''),
            'delivery_address' : request.POST.get('delivery_address',''),
            'delivery_city' : request.POST.get('delivery_city',''),
            'delivery_state' : request.POST.get('delivery_state',''),
            'delivery_zip' : request.POST.get('delivery_zip',''),
            'delivery_country' : request.POST.get('delivery_country',''),
            'delivery_tel' : request.POST.get('delivery_tel',''),
            'merchant_param1' : request.POST.get('merchant_param1',''),
            'merchant_param2' : request.POST.get('merchant_param2',''),
            'merchant_param3' : request.POST.get('merchant_param3',''),
            'merchant_param4' : request.POST.get('merchant_param4',''),
            'merchant_param5' : request.POST.get('merchant_param5',''),
            'promo_code' : request.POST.get('promo_code',''),
            'customer_identifier': request.POST.get('customer_identifier', '')
        }

        # Creating the merchant data string
        merchant_data = '&'.join([f'{key}={value}' for key, value in form_data.items()])

        # Encrypting the merchant data
        encryption = encrypt(merchant_data, workingKey)

        # HTML template
        html_template = '''
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
            <form id="nonseamless" method="post" name="redirect" action="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction">
                <input type="hidden" id="encRequest" name="encRequest" value="$encReq">
                <input type="hidden" name="access_code" id="access_code" value="$xscode">
                <script language='javascript'>document.redirect.submit();</script>
            </form>
        </body>
        </html>
        '''

        # Substituting values into the HTML template
        html_content = Template(html_template).safe_substitute(encReq=encryption, xscode=accessCode)

        return HttpResponse(html_content)
    return HttpResponse("Invalid Request")
